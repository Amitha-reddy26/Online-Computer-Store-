# Online Computer Store

A portfolio implementation of an academic database
management project using Python and MySQL.

## Features

- Relational database with five normalized tables
- Primary and foreign key constraints
- Product and inventory management
- Transaction-based order processing
- Stock validation and transaction rollback
- SQL joins and aggregate queries
- Inventory and sales reports
- Automated quantity validation tests
- GitHub Actions CI

## Technologies

Python, MySQL, SQL, Pandas, Docker, Pytest,
Git and GitHub Actions.

## Usage

Install dependencies:

    pip install -r requirements.txt

Configure a MySQL database named online_computer_store
with user store_user on localhost port 3307.
Set STORE_DB_PASSWORD in your environment.

    python src/store.py init
    python src/store.py products
    python src/store.py order --customer 1 --product 2 --quantity 1
    python src/store.py report
    python -m pytest -v

## Database Design

Categories, Products, Customers, Orders and Order Items.

The application uses parameterized SQL queries and
database transactions to maintain inventory consistency.

## Project Note

This is a simplified portfolio implementation created
in November 2026 based on an earlier academic project.
The sample customer and product data are illustrative.
