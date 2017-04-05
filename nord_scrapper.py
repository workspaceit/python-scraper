import mysql.connector
import requests
import validators
from bs4 import BeautifulSoup
import time
import re
import selenium.webdriver as webdriver
import contextlib

phantomjs = 'phantomjs'



cnx = mysql.connector.connect(user='root', password='', host='localhost', database='awesome_store')
cursor = cnx.cursor()
base_url = 'http://shop.nordstrom.com'
product_type = {
    'women': 1,
    'men': 2,
    'home': 3,
    'kids': 4
}

def scrap_product_page(product_soup, sub_category,p_type):
    # products = product_soup.find_all(class_='npr-result-set')
    # if products:
    #     for tgt_product in products:
    pro_thum=product_soup.select('div.npr-gallery-item')
    print 'total'
    print len(pro_thum)
    for tgt_pro_thum in pro_thum:
        #Get Product Image
        product_image= tgt_pro_thum.find(class_='product-photo').get('src')
        #Get Product Name
        product_name= tgt_pro_thum.find(class_='product-title').select("a span")[0].string
        #Get product Price
        #product_price= tgt_pro_thum.find(class_='original-price').select("span")[0].string
        product_price= tgt_pro_thum.find(class_='original-price').select(".price")[0].string
        #product_price = product_price.replace("BDT ", "")

        # if product_price.find("-") != -1:
        #     print "Valid"
        # else:
        #     product_price = product_price.replace("BDT ", "")
        #     product_price = product_price.replace(",", "")
        #     product_price = float(product_price) / 86.4479710145

        # print product_price
        # print "\n"
        # print type(product_price)
        #product_price=float(product_price)/86.4479710145


        #Get Product Url
        product_url= tgt_pro_thum.find(class_='product-title').find('a').get('href')
        product_urls=product_url.split('?')
        product_urls= product_urls[0].split('/')
        product_id=product_urls[-1]
        if not validators.url(product_url):
            product_url=base_url+product_url

        # print p_id
        # print title
        # print price
        # print img_src
        # print full_link

        category_id = product_type[p_type]

        sql = "INSERT INTO products(identifier, title, image, category_id,sub_category_name, price, site_id, details_url) VALUES " \
              "('%s', '%s', '%s', '%d', '%s','%s', '%d', '%s')" % ( product_id, re.escape(product_name), product_image, category_id, re.escape(sub_category),product_price, 3, product_url)
        try:
            cursor.execute(sql)
            cnx.commit()
        except Exception as e:
            cnx.rollback()
            print e
            # break

def start_scrapper():
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    menu = soup.find(id='rfx-desktop-global-nav')
    menu_anchors = menu.select('.rfx_T-B-F')

    for tgt in menu_anchors:
        p_type = tgt.string.lower()
        if p_type == 'women' or p_type == 'men' or p_type == 'kids' or p_type == 'home':
            partial_link = tgt.get('href')
            link = base_url + partial_link
            category_page = requests.get(link)
            category_page_soup = BeautifulSoup(category_page.content, 'html.parser')

            if p_type == 'women':
                sub_menu = category_page_soup.find(id='category-nav')
                sub_anchors = sub_menu.select('li a')
                print 'women'
                print len(sub_anchors)
            else:
                sub_menu = category_page_soup.find(class_='side-navigation')
                sub_anchors = sub_menu.select('li a')
                print 'other'
                print len(sub_anchors)

            for sub_tgt in sub_anchors:
                sub_partial_link = sub_tgt.get('href')
                sub_category=sub_tgt.string

                if not validators.url(sub_partial_link):
                    sub_partial_link=base_url+sub_partial_link

                print "Subcategory"
                print sub_partial_link
                print "Subcategory"

                try:
                    with contextlib.closing(webdriver.PhantomJS(phantomjs)) as driver:
                        driver.get(sub_partial_link)
                        content = driver.page_source
                        product_list_page_soup = BeautifulSoup(content, 'html.parser')
                        print 'mind'
                        scrap_product_page(product_list_page_soup,sub_category,p_type)
                except:
                    print("Connection refused by the server..")
                    continue


start_scrapper()

