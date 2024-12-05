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


class Ethnicity(Base):
    """description: Holds all ethnic styles of cooking"""
    __tablename__ = 'ethnicity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class SpiceLevel(Base):
    """description: Specifies levels of spice for the recipes"""
    __tablename__ = 'spice_level'
    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String, nullable=False)


class Cookbook(Base):
    """description: Defines cookbooks, their titles, and associations with ethnic styles"""
    __tablename__ = 'cookbook'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    ethnicity_id = Column(Integer, ForeignKey('ethnicity.id'))


class Chef(Base):
    """description: Details of chefs who conduct cooking classes"""
    __tablename__ = 'chef'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_disabled = Column(Boolean, nullable=False)


class CookingClass(Base):
    """description: Information about cooking classes offered, linked to chefs"""
    __tablename__ = 'cooking_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_date = Column(Date)
    chef_id = Column(Integer, ForeignKey('chef.id'))
    charity_percentage = Column(Integer, nullable=False)


class Recipe(Base):
    """description: Contains recipes, linking them to specific cookbooks and spice levels"""
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cookbook_id = Column(Integer, ForeignKey('cookbook.id'))
    spice_level_id = Column(Integer, ForeignKey('spice_level.id'))


class Sale(Base):
    """description: Tracks sales of cookbooks and tickets to cooking classes"""
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_of_sale = Column(Date)
    cookbook_id = Column(Integer, ForeignKey('cookbook.id'), nullable=True)
    cooking_class_id = Column(Integer, ForeignKey('cooking_class.id'), nullable=True)
    amount = Column(Integer, nullable=False)


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    ethnicity1 = Ethnicity(id=1, name="Mexican")
    ethnicity2 = Ethnicity(id=2, name="Italian")
    ethnicity3 = Ethnicity(id=3, name="Chinese")
    ethnicity4 = Ethnicity(id=4, name="Indian")
    spice_level1 = SpiceLevel(id=1, level="Mild")
    spice_level2 = SpiceLevel(id=2, level="Medium")
    spice_level3 = SpiceLevel(id=3, level="Hot")
    spice_level4 = SpiceLevel(id=4, level="Extra Hot")
    cookbook1 = Cookbook(id=1, title="Fiesta Flavors", ethnicity_id=1)
    cookbook2 = Cookbook(id=2, title="Roman Recipes", ethnicity_id=2)
    cookbook3 = Cookbook(id=3, title="Oriental Delights", ethnicity_id=3)
    cookbook4 = Cookbook(id=4, title="Spicy Delicacies", ethnicity_id=4)
    chef1 = Chef(id=1, name="Chef Ramon", is_disabled=True)
    chef2 = Chef(id=2, name="Chef Maria", is_disabled=False)
    chef3 = Chef(id=3, name="Chef Wei Ling", is_disabled=True)
    chef4 = Chef(id=4, name="Chef Vijay", is_disabled=False)
    cooking_class1 = CookingClass(id=1, class_date=date(2023, 5, 22), chef_id=1, charity_percentage=10)
    cooking_class2 = CookingClass(id=2, class_date=date(2023, 6, 18), chef_id=2, charity_percentage=15)
    cooking_class3 = CookingClass(id=3, class_date=date(2023, 7, 25), chef_id=3, charity_percentage=20)
    cooking_class4 = CookingClass(id=4, class_date=date(2023, 8, 19), chef_id=4, charity_percentage=12)
    recipe1 = Recipe(id=1, name="Mild Enchiladas", cookbook_id=1, spice_level_id=1)
    recipe2 = Recipe(id=2, name="Spaghetti Bolognese", cookbook_id=2, spice_level_id=2)
    recipe3 = Recipe(id=3, name="Kung Pao Chicken", cookbook_id=3, spice_level_id=3)
    recipe4 = Recipe(id=4, name="Vindaloo Lamb", cookbook_id=4, spice_level_id=4)
    sale1 = Sale(id=1, date_of_sale=date(2023, 5, 23), cookbook_id=1, cooking_class_id=None, amount=30)
    sale2 = Sale(id=2, date_of_sale=date(2023, 6, 19), cookbook_id=None, cooking_class_id=2, amount=45)
    sale3 = Sale(id=3, date_of_sale=date(2023, 7, 26), cookbook_id=3, cooking_class_id=None, amount=35)
    sale4 = Sale(id=4, date_of_sale=date(2023, 8, 20), cookbook_id=None, cooking_class_id=4, amount=50)
    
    
    
    session.add_all([ethnicity1, ethnicity2, ethnicity3, ethnicity4, spice_level1, spice_level2, spice_level3, spice_level4, cookbook1, cookbook2, cookbook3, cookbook4, chef1, chef2, chef3, chef4, cooking_class1, cooking_class2, cooking_class3, cooking_class4, recipe1, recipe2, recipe3, recipe4, sale1, sale2, sale3, sale4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
