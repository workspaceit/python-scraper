import mysql.connector
import requests
import validators
from bs4 import BeautifulSoup

from crawler import identifier

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='awesome_store')
cursor = cnx.cursor()
base_url = 'https://www.macys.com'
product_type = {
    'women': 1,
    'men': 2,
    'home': 3,
    'kids': 4
}


def scrap_product_page(product_soup, p_type):
    products = product_soup.find_all(class_='productThumbnail')

    for p in products:
        p_id = p.get('id')
        title_with_extra = p.find(class_='shortDescription').find('a').string
        if title_with_extra is not None:
            title = title_with_extra.strip('\n')
            current_price_tag = p.find(class_='colorway-price').find_all(class_='first-range')[0]
            price_with_extra = current_price_tag.string
            price = price_with_extra.strip('\n')
            price = price.replace('$', '')

            img_src = p.find(class_='thumbnailImage').get('data-src')


            link = p.find(class_='productThumbnailLink').get('href')
            #link_one = p.find(identifier='mainView_1').get('href')
            #print link_one
            full_link = base_url + link

            img_name_db = 'p_image_' + p_id + '.jpg'
            img_name = 'product_images/' + img_name_db
            with open(img_name, "wb") as f:
                #print("anik")
                requests.get(img_src)
                f.write(requests.get(img_src).content)

            # print p_id
            # print title
            # print price
            # print img_src
            # print full_link

            store_id = product_type[p_type]

            sql = "INSERT INTO products(identifier, title, image, store_id, price, site_id, details_url) VALUES " \
                  "('%s', '%s', '%s', '%d', '%s', '%d', '%s')" % (p_id, title, img_src, store_id, price, 2, full_link)
            try:
                cursor.execute(sql)
                cnx.commit()
            except:
                cnx.rollback()
            # break


def start_scrapper():
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    menu = soup.find(id='globalMastheadCategoryMenu')
    anchors = menu.select('li a')
    anchors.pop()
    for anchor in anchors:
        p_type = anchor.string.lower()
        if p_type == 'women' or p_type == 'men' or p_type == 'kids' or p_type == 'home':
            partial_link = anchor.get('href')
            link = base_url + partial_link
            print('------' + link + '--------')
            category_page = requests.get(link)
            category_page_soup = BeautifulSoup(category_page.content, 'html.parser')

            first_ul = category_page_soup.find(id='firstNavSubCat')

            sub_anchors = first_ul.select('.nav_cat_item_bold ul li a')
            sub_anchors2 = first_ul.select('.nav_cat_item_hilite a')
            sub_anchors = sub_anchors + sub_anchors2

            for sub_anchor in sub_anchors:
                #List of sub category
                sub_partial_link = sub_anchor.get('href')
                print(sub_partial_link)
                product_list_page = requests.get(sub_partial_link)
                #list of product
                product_list_page_soup = BeautifulSoup(product_list_page.content, 'html.parser')
                scrap_product_page(product_list_page_soup, p_type)

start_scrapper()






