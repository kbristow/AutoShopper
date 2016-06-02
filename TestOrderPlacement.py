from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Models.product import Product
import Settings

__author__ = 'BristK'


def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def load_page(driver, page_link):
    driver.execute_script("window.location='"+page_link+"'")


def add_product_to_cart(driver, product, quantity):
    driver.execute_script('function addCatalogItemToBasketPNPSHOPPER(itemKey, areaKey, quantity) {'
                          '      var postData = {'
                          '          itemKey: [ 1 ],'
                          '          itemQuantity: [ 1 ],'
                          '          areaKey: [ 1 ]'
                          '      };'
                          '      postData.itemKey[0] = itemKey;'
                          '      postData.itemQuantity[0] = quantity;'
                          '      postData.areaKey[0] = areaKey;'
                          '      $.ajax({'
                          '          type: "POST",'
                          '          dataType: "json",'
                          '          url: "/b2c_pnp/addtobasket",'
                          '          data: "postData=" + JSON.stringify(postData)'
                          '      })'
                          '      .done(function (basket) {'
                          '          basket["error"] = "";'
                          '          basket["errorText"] = "";'
                          '          updateMinibasket(basket);'
                          '      })'
                          '      .fail(function (jqXHR, textStatus) {'
                          '          alert(textStatus);'
                          '      });'
                          ' };'
                          'addCatalogItemToBasketPNPSHOPPER("'+product.pnp_product_code+'", "' +
                          product.pnp_category_code +
                          '","' + str(quantity) + '");')

driver = init_driver()
driver.get("http://shop.pnp.co.za")
driver.execute_script('login_action();')

username = Settings.username()
password = Settings.password()

driver.execute_script('$("#j_username").val("'+username+'");')
driver.execute_script('$("#j_password").val("'+password+'");')
driver.execute_script('$("#loginButton").click();')

engine = create_engine('sqlite:///pnpshopper.db')
Base = declarative_base()
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

product = session.query(Product).filter(Product.id == 2).first()
add_product_to_cart(driver, product, 6)

product = session.query(Product).filter(Product.id == 3).first()
add_product_to_cart(driver, product, 10)

product = session.query(Product).filter(Product.id == 4).first()
add_product_to_cart(driver, product, 3)
