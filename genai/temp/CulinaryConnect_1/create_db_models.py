# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class Ethnicity(Base):\n    '''\n    description: Table storing available ethnicities for cookbooks.\n    '''\n    __tablename__ = 'ethnicity'\n\n    id = Column(Integer, primary_key=True, autoincrement=True)\n    name = Column(String, nullable=False)


class SpiceLevel(Base):\n    '''\n    description: Table holding different spice levels for recipes.\n    '''\n    __tablename__ = 'spice_level'\n\n    id = Column(Integer, primary_key=True, autoincrement=True)\n    level = Column(String, nullable=False)


class Charity(Base):\n    '''\n    description: Table listing charities that receive part of the cooking class profits.\n    '''\n    __tablename__ = 'charity'\n\n    id = Column(Integer, primary_key=True, autoincrement=True)\n    name = Column(String, nullable=False)\n    cause = Column(String)


class Chef(Base):\n    '''\n    description: Table with the details of chefs, some of whom may be disabled.\n    '''\n    __tablename__ = 'chef'\n\n    id = Column(Integer, primary_key=True, autoincrement=True)\n    name = Column(String, nullable=False)\n    is_disabled = Column(Boolean)


class CookingClass(Base):\n    '''\n    description: Table holding details of cooking classes offered.\n    '''\n    __tablename__ = 'cooking_class'\n\n    id = Column(Integer, primary_key=True, autoincrement=True)\n    title = Column(String, nullable=False)\n    date = Column(Date, nullable=False)\n    charity_id = Column(Integer, ForeignKey('charity.id'))\n    chef_id = Column(Integer, ForeignKey('chef.id'))


class Cookbook(Base):\n    '''\n    description: Table representing available cookbooks.\n    '''\n    __tablename__ = 'cookbook'\n\n    id = Column(Integer, primary_key=True, autoincrement=True)\n    title = Column(String, nullable=False)\n    price = Column(Integer, nullable=False)\n    ethnicity_id = Column(Integer, ForeignKey('ethnicity.id'))\n    spice_level_id = Column(Integer, ForeignKey('spice_level.id'))


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    charity1 = Charity(name='FoodForAll', cause='Support culinary education for children')
    charity2 = Charity(name='ChefAid', cause='Professional development for disabled chefs')
    charity3 = Charity(name='FeedTheHungry', cause='Combating hunger worldwide')
    charity4 = Charity(name='CanCook', cause='Supporting disabled individuals')
    chef1 = Chef(name='John Doe', is_disabled=True)
    chef2 = Chef(name='Jane Smith', is_disabled=False)
    chef3 = Chef(name='Carlos Motta', is_disabled=True)
    chef4 = Chef(name='Ryu Tanaka', is_disabled=False)
    cooking_class1 = CookingClass(title='Mexican Fiesta', date=date(2023, 5, 15), charity_id=1, chef_id=1)
    cooking_class2 = CookingClass(title='Mastering\u200c Spices', date=date(2023, 6, 20), charity_id=2, chef_id=2)
    cooking_class3 = CookingClass(title='Gourmet Delights', date=date(2023, 7, 10), charity_id=3, chef_id=3)
    cooking_class4 = CookingClass(title='Vegan Cooking', date=date(2023, 8, 25), charity_id=4, chef_id=4)
    cookbook1 = Cookbook(title='Tacos and More', price=29, ethnicity_id=1, spice_level_id=2)
    cookbook2 = Cookbook(title='Indian Curries', price=35, ethnicity_id=2, spice_level_id=3)
    cookbook3 = Cookbook(title='Italian Classics', price=25, ethnicity_id=3, spice_level_id=1)
    cookbook4 = Cookbook(title='Spicy Wonders', price=40, ethnicity_id=4, spice_level_id=4)
    ethnicity1 = Ethnicity(name='Mexican')
    ethnicity2 = Ethnicity(name='Indian')
    ethnicity3 = Ethnicity(name='Italian')
    ethnicity4 = Ethnicity(name='Korean')
    spice_level1 = SpiceLevel(level='Mild')
    spice_level2 = SpiceLevel(level='Medium')
    spice_level3 = SpiceLevel(level='Hot')
    spice_level4 = SpiceLevel(level='Extra Hot')
    
    
    
    session.add_all([charity1, charity2, charity3, charity4, chef1, chef2, chef3, chef4, cooking_class1, cooking_class2, cooking_class3, cooking_class4, cookbook1, cookbook2, cookbook3, cookbook4, ethnicity1, ethnicity2, ethnicity3, ethnicity4, spice_level1, spice_level2, spice_level3, spice_level4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
