import os
import argparse
from pathlib import Path
import mysql.connector
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def connect():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="store_user",
        password=os.environ["STORE_DB_PASSWORD"],
        database="online_computer_store"
    )

def initialize():
    with connect() as conn:
        cursor = conn.cursor()
        schema = (ROOT / "sql/schema.sql").read_text()
        for statement in schema.split(";"):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        print("Database initialized successfully!")

def validate_quantity(quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    return quantity

def place_order(customer, product, quantity):
    validate_quantity(quantity)
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT price, stock FROM products "
                "WHERE product_id=%s FOR UPDATE",
                (product,)
            )
            row = cursor.fetchone()
            if not row or row[1] < quantity:
                raise ValueError("Insufficient stock or invalid product")

            cursor.execute(
                "INSERT INTO orders(customer_id) VALUES (%s)",
                (customer,)
            )
            order_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO order_items VALUES (%s,%s,%s,%s)",
                (order_id, product, quantity, row[0])
            )

            cursor.execute(
                "UPDATE products SET stock=stock-%s "
                "WHERE product_id=%s",
                (quantity, product)
            )

            conn.commit()
            print(f"Order {order_id} created successfully!")
        except Exception:
            conn.rollback()
            raise

def query(sql, params=()):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=cursor.column_names
        )

def products():
    print(query("SELECT * FROM products").to_string(index=False))

def report():
    inventory = query("""
        SELECT c.name AS category,
               COUNT(*) AS products,
               SUM(p.stock) AS total_stock,
               SUM(p.stock*p.price) AS inventory_value
        FROM products p
        JOIN categories c USING(category_id)
        GROUP BY c.name
    """)

    sales = query("""
        SELECT p.name,
               SUM(i.quantity) AS units_sold,
               SUM(i.quantity*i.unit_price) AS revenue
        FROM order_items i
        JOIN products p USING(product_id)
        GROUP BY p.product_id, p.name
    """)

    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)
    inventory.to_csv(output / "inventory.csv", index=False)
    sales.to_csv(output / "sales.csv", index=False)
    print(inventory.to_string(index=False))
    print(sales.to_string(index=False))
    print("Reports saved successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action",
        choices=["init", "products", "order", "report"]
    )
    parser.add_argument("--customer", type=int, default=1)
    parser.add_argument("--product", type=int, default=1)
    parser.add_argument("--quantity", type=int, default=1)
    args = parser.parse_args()

    if args.action == "init":
        initialize()
    elif args.action == "products":
        products()
    elif args.action == "order":
        place_order(args.customer, args.product, args.quantity)
    elif args.action == "report":
        report()
