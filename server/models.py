from config import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy import DateTime 

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-sales.user',)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    role = db.Column(db.String)

    sales = db.relationship('Sales', back_populates='user')

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    serialize_rules = ('-sales.product', '-stock.product', '-sales.user',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Float)
    stock_level = db.Column(db.Integer)
    
    sales = db.relationship('Sales', back_populates="product", cascade='all, delete-orphan')
    stock = db.relationship('Stock', back_populates="product", cascade='all, delete-orphan')

class Sales(db.Model, SerializerMixin):
    __tablename__ ='sales'

    serialize_rules = ('-user.sales', '-product.sales',)
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    date = db.Column(DateTime, default=datetime.now)

    product = db.relationship('Product', back_populates="sales")
    user = db.relationship('User', back_populates='sales')

class Stock(db.Model, SerializerMixin):
    __tablename__ ='stock'

    serialize_rules = ('-product.stock',)
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity_added = db.Column(db.Integer)
    date = db.Column(DateTime, default=datetime.now)

    product = db.relationship('Product', back_populates="stock")