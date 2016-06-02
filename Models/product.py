from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, ForeignKey

__author__ = 'BristK'

Base = declarative_base()


class ProductCategory(Base):
    __tablename__ = 'ProductCategory'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    web_link = Column(String)


class ProductType(Base):
    __tablename__ = 'ProductType'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    raw_name = Column(String)
    name = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey(ProductCategory.id))
    category = relationship(ProductCategory)
    pnp_category_code = Column(String)
    pnp_product_code = Column(String)
    type_id = Column(Integer, ForeignKey(ProductType.id))
    type = relationship(ProductType)



