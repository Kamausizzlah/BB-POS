from faker import Faker
from config import db, app 
from models import Product, Sales, Stock, User 
import random


faker = Faker()

NUM_PRODUCTS = 10
NUM_USERS = 5
NUM_SALES = 50
NUM_STOCK_ENTRIES = 30

def create_products():
    try:
        products = []
        for _ in range(NUM_PRODUCTS):
            product = Product(
                name=faker.word(),
                category=faker.random_element(elements=('Electronics', 'Clothing', 'Groceries', 'Books', 'Toys')),
                price=round(random.uniform(10.0, 500.0), 2),
                stock_level=random.randint(1, 100)
            )
            products.append(product)
            db.session.add(product)
        db.session.commit()
        return products
    except Exception as e:
        print(f"Error creating products: {e}")
        db.session.rollback()

def create_users():
    try:
        users = []
        for _ in range(NUM_USERS):
            user = User(
                username=faker.name(),
                email=faker.email(),
                password_hash=faker.password()
            )
            users.append(user)
            db.session.add(user)
        db.session.commit()
        return users
    except Exception as e:
        print(f"Error creating users: {e}")
        db.session.rollback()

def create_sales(products, users):
    try:
        for _ in range(NUM_SALES):
            sale = Sales(
                product_id=random.choice(products).id,
                user_id=random.choice(users).id,
                quantity=random.randint(1, 5),
                total_price=round(random.uniform(20.0, 1000.0), 2),
                date=faker.date_time_this_year()
            )
            db.session.add(sale)
        db.session.commit()
    except Exception as e:
        print(f"Error creating sales: {e}")
        db.session.rollback()

def create_stock_entries(products):
    try:
        for _ in range(NUM_STOCK_ENTRIES):
            stock = Stock(
                product_id=random.choice(products).id,
                quantity_added=random.randint(10, 200),
                date=faker.date_time_this_year()
            )
            db.session.add(stock)
        db.session.commit()
    except Exception as e:
        print(f"Error creating stock entries: {e}")
        db.session.rollback()

def main():
    print("Seeding database...")
    
    users = create_users()
    products = create_products()
    create_sales(products, users)
    create_stock_entries(products)
    
    print("Database seeding complete!")

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        main()
