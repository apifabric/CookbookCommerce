# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    """
    description: Table for storing customer information including their balance and credit limit.
    """
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    balance = Column(Float, nullable=True, default=0.0)
    credit_limit = Column(Float, nullable=False, default=0.0)
    
    orders = relationship("Order", back_populates="customer")


class Order(Base):
    """
    description: Table for storing orders placed by customers, includes notes and shipment status.
    """
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    amount_total = Column(Float, nullable=True, default=0.0)
    date_shipped = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    
    customer = relationship("Customer", back_populates="orders")
    items = relationship("Item", back_populates="order")


class Item(Base):
    """
    description: Table for storing individual items in an order, including calculated amount.
    """
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=True, default=0.0)
    amount = Column(Float, nullable=True, default=0.0)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")


class Product(Base):
    """
    description: Table for storing product information including the unit price.
    """
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    items = relationship("Item", back_populates="product")

# Setup the database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite', echo=False)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data for testing
product1 = Product(name="Laptop", unit_price=1000.0)
product2 = Product(name="Mouse", unit_price=20.0)

customer1 = Customer(name="John Doe", credit_limit=5000.0, balance=0.0)
customer2 = Customer(name="Jane Smith", credit_limit=3000.0, balance=0.0)

order1 = Order(customer_id=1, date_shipped=None, notes="Urgent order")
order2 = Order(customer_id=2, date_shipped=datetime.now(), notes="")

item1 = Item(order_id=1, product_id=1, quantity=1, unit_price=1000.0, amount=1000.0)
item2 = Item(order_id=1, product_id=2, quantity=2, unit_price=20.0, amount=40.0)
item3 = Item(order_id=2, product_id=2, quantity=5, unit_price=20.0, amount=100.0)

# Add data to session
session.add_all([product1, product2, customer1, customer2, order1, order2, item1, item2, item3])
session.commit()

# Initialize derived attributes
# Order.amount_total
order1.amount_total = item1.amount + item2.amount
order2.amount_total = item3.amount

# Customer.balance
customer1.balance = order1.amount_total if order1.date_shipped is None else 0
customer2.balance = order2.amount_total if order2.date_shipped is None else 0

session.commit()

def declare_logic():
    Rule.sum(derive=Customer.balance, as_sum_of=Order.amount_total, where=lambda row: row.date_shipped is None)
    Rule.sum(derive=Order.amount_total, as_sum_of=Item.amount)
    Rule.formula(derive=Item.amount, as_expression=lambda row: row.quantity * row.unit_price)
    Rule.copy(derive=Item.unit_price, from_parent=Product.unit_price)
    Rule.constraint(validate=Customer,
                    as_condition=lambda row: row.balance <= row.credit_limit,
                    error_msg="Customer balance ({row.balance}) exceeds credit limit ({row.credit_limit})")
