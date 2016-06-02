from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Models.product import ProductCategory, Product
import re


def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver
 

set_view_all_done = False


def set_view_all(driver):
    global set_view_all_done
    if not set_view_all_done:
        driver.execute_script("setPageSize(0)")
        set_view_all_done = True


def find_pnp_grocery_categories(driver):
    driver.get(
        "http://shop.pnp.co.za/b2c_pnp/b2c/display/%28cpgnum=1&layout=5.1-6_2_4_86_87_8_3&uiarea=1" +
        "&carea=4F3CED2FF4A28570E10080000A050131&cpgsize=12%29/.do?rf=y")

    result = driver.execute_script('var returnStructure=[];'
                                   'var shoppingLinks=$($("#menuListShopping>'
                                   '#menuListShoppingHolder0>'
                                   '.menuListShopping-drop")[0])'
                                   '.find("[id^=menuListShoppingHolder]>a");'
                                   'for(var i = 0; i < shoppingLinks.length;i++){'
                                   'var jQueryElement=$(shoppingLinks[i]);'
                                   'returnStructure.push({'
                                   '    "name":jQueryElement.text(),'
                                   '    "link":jQueryElement.attr("href")});'
                                   '}'
                                   'return returnStructure;')
    return result


def load_page(driver, page_link):
    driver.execute_script("window.location='"+page_link+"'")
    set_view_all(driver)


def extract_price(price_string):
    new_price = ""
    for character in price_string:
        if character.isdigit():
            new_price += character

    return float(new_price)/100


def extract_pnp_product_codes(onclick_string):
    regex_pattern = r"addCatalogItemToBasket\('productform', '([\s\S]*?)', '([\s\S]*?)'"
    pnp_details_result = re.search(regex_pattern, onclick_string, re.M | re.I)
    pnp_product_code = ""
    pnp_category_code = ""
    if pnp_details_result:
        pnp_product_code = pnp_details_result.group(1)
        pnp_category_code = pnp_details_result.group(2)
    return pnp_product_code, pnp_category_code


def extract_products_from_page(driver):
    result = driver.execute_script('var results=[];'
                                   'var productNames = $(".productName>a");'
                                   'var productPrices = $(".unitPriceDetails>.unitPrice");'
                                   'var productAddDetails = $(".productFunctionality>a");'
                                   'for (var i = 0; i < productNames.length; i ++){'
                                   'results.push({'
                                   '    "name":$(productNames[i]).attr("title"), '
                                   '    "price":$(productPrices[i]).text(), '
                                   '    "pnp_onclick":$(productAddDetails[i]).attr("onclick")'
                                   '})'
                                   '}'
                                   'return results;')

    for product in result:
        product["price"] = extract_price(product["price"])
        product["pnp_product_code"], product["pnp_category_code"] = extract_pnp_product_codes(product["pnp_onclick"])

    return result

if __name__ == "__main__":
    engine = create_engine('sqlite:///pnpshopper.db')
    Base = declarative_base()
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    session.query(Product).delete()
    session.query(ProductCategory).delete()

    driver = init_driver()
    grocery_pages = find_pnp_grocery_categories(driver)
    count = 0
    for page in grocery_pages:
        new_category = ProductCategory(name=page["name"], web_link=page["link"])
        session.add(new_category)
        # 'if count < 1:
        load_page(driver, page["link"])
        results = extract_products_from_page(driver)

        for product in results:
            new_product = Product(raw_name=product["name"], price=product["price"], category=new_category,
                                  pnp_product_code=product["pnp_product_code"],
                                  pnp_category_code=product["pnp_category_code"])
            session.add(new_product)
        # 'count += 1
    session.commit()
