from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Models.product import ProductCategory, Product


engine = create_engine('sqlite:///pnpshopper.db')
Base = declarative_base()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

results = session.query(ProductCategory).all()
products = session.query(Product).all()

print "Done"
