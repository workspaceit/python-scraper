import mysql.connector
import requests
import validators
from bs4 import BeautifulSoup
import re

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='awesome_store')
cursor = cnx.cursor()
base_url = 'https://www.gilt.com'
product_type = {
    'women': 1,
    'men': 2,
    'home': 3,
    'kids': 4
}


def scrap_product_page(product_soup, sub_category,p_type):

    product_list=product_soup.select('.product-look')
    for tgt_product_list in product_list:
        product_id= tgt_product_list.get('data-gilt-look-id')
        product_url= tgt_product_list.select('a')[0].get('href')
        product_name_two= tgt_product_list.select('.brand-name-text')[0].string
        product_name_one= tgt_product_list.select('.product-name a')[0].string
        product_name=product_name_two+product_name_one
        product_image= tgt_product_list.find('picture').find('img').get('src')
        product_price= tgt_product_list.select('.price')[0].string

        category_id = product_type[p_type]

        sql = "INSERT INTO products(identifier, title, image, category_id,sub_category_name, price, site_id, details_url) VALUES " \
              "('%s', '%s', '%s', '%d', '%s','%s', '%d', '%s')" % (
              product_id, re.escape(product_name), product_image, category_id, re.escape(sub_category), product_price,1, product_url)
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
    menu = soup.find(class_='store-tabs')
    menus=menu.select('.tab')
    for tgt_menu in menus:
        p_type=tgt_menu.select("a span")[0].string.lower()
        if p_type == 'women' or p_type == 'men' or p_type == 'kids' or p_type == 'home':
            subs_div=tgt_menu.select('.nav-categories .menu-action')

            print len(subs_div)

            for tgt_subs_div in subs_div:
                sub_category= tgt_subs_div.select("a")[0].string
                subs_category_urls= tgt_subs_div.select('a')[0].get('href')

                if not validators.url(subs_category_urls):
                    sub_partial_link=base_url+subs_category_urls

                try:
                    product_list_page = requests.get(sub_partial_link)
                    # list of product
                    product_list_page_soup = BeautifulSoup(product_list_page.content, 'html.parser')
                    scrap_product_page(product_list_page_soup, sub_category, p_type)
                except:
                    print("Connection refused by the server..")
                    #continue


start_scrapper()






