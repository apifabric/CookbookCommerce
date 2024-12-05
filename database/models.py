# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 05, 2024 14:57:29
# Database: sqlite:////tmp/tmp.D1OlOpUQ3A-01JEBN3GJJ6QJZM68JGMYQRZFG/CulinaryConnect/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Chef(SAFRSBaseX, Base):
    """
    description: Details of chefs who conduct cooking classes
    """
    __tablename__ = 'chef'
    _s_collection_name = 'Chef'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_disabled = Column(Boolean, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    CookingClassList : Mapped[List["CookingClass"]] = relationship(back_populates="chef")



class Ethnicity(SAFRSBaseX, Base):
    """
    description: Holds all ethnic styles of cooking
    """
    __tablename__ = 'ethnicity'
    _s_collection_name = 'Ethnicity'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    CookbookList : Mapped[List["Cookbook"]] = relationship(back_populates="ethnicity")



class SpiceLevel(SAFRSBaseX, Base):
    """
    description: Specifies levels of spice for the recipes
    """
    __tablename__ = 'spice_level'
    _s_collection_name = 'SpiceLevel'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    RecipeList : Mapped[List["Recipe"]] = relationship(back_populates="spice_level")



class Cookbook(SAFRSBaseX, Base):
    """
    description: Defines cookbooks, their titles, and associations with ethnic styles
    """
    __tablename__ = 'cookbook'
    _s_collection_name = 'Cookbook'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    ethnicity_id = Column(ForeignKey('ethnicity.id'))

    # parent relationships (access parent)
    ethnicity : Mapped["Ethnicity"] = relationship(back_populates=("CookbookList"))

    # child relationships (access children)
    RecipeList : Mapped[List["Recipe"]] = relationship(back_populates="cookbook")
    SaleList : Mapped[List["Sale"]] = relationship(back_populates="cookbook")



class CookingClass(SAFRSBaseX, Base):
    """
    description: Information about cooking classes offered, linked to chefs
    """
    __tablename__ = 'cooking_class'
    _s_collection_name = 'CookingClass'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    class_date = Column(Date)
    chef_id = Column(ForeignKey('chef.id'))
    charity_percentage = Column(Integer, nullable=False)

    # parent relationships (access parent)
    chef : Mapped["Chef"] = relationship(back_populates=("CookingClassList"))

    # child relationships (access children)
    SaleList : Mapped[List["Sale"]] = relationship(back_populates="cooking_class")



class Recipe(SAFRSBaseX, Base):
    """
    description: Contains recipes, linking them to specific cookbooks and spice levels
    """
    __tablename__ = 'recipe'
    _s_collection_name = 'Recipe'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cookbook_id = Column(ForeignKey('cookbook.id'))
    spice_level_id = Column(ForeignKey('spice_level.id'))

    # parent relationships (access parent)
    cookbook : Mapped["Cookbook"] = relationship(back_populates=("RecipeList"))
    spice_level : Mapped["SpiceLevel"] = relationship(back_populates=("RecipeList"))

    # child relationships (access children)



class Sale(SAFRSBaseX, Base):
    """
    description: Tracks sales of cookbooks and tickets to cooking classes
    """
    __tablename__ = 'sale'
    _s_collection_name = 'Sale'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    date_of_sale = Column(Date)
    cookbook_id = Column(ForeignKey('cookbook.id'))
    cooking_class_id = Column(ForeignKey('cooking_class.id'))
    amount = Column(Integer, nullable=False)

    # parent relationships (access parent)
    cookbook : Mapped["Cookbook"] = relationship(back_populates=("SaleList"))
    cooking_class : Mapped["CookingClass"] = relationship(back_populates=("SaleList"))

    # child relationships (access children)
