import mysql.connector
import requests
import validators
from bs4 import BeautifulSoup
from os.path import basename
from decimal import Decimal



cnx = mysql.connector.connect(user='root', password='1', host='localhost', database='awesome_store')
cursor = cnx.cursor()
base_url = 'https://www.macys.com'


def scrap_product_page(product_soup):
    return
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
            price = Decimal(price)

            img_src = p.find(class_='thumbnailImage').get('data-src')

            link = p.find(class_='productThumbnailLink').get('href')
            full_link = base_url + link

            img_name = 'p_image_' + p_id + '.jpg'
            with open(basename(img_name), "wb") as f:
                f.write(requests.get(img_src).content)

            print p_id
            print title
            print price
            print img_src
            print full_link

            sql = "INSERT INTO products(identifier, title, image, price, details_url) VALUES ('%s', '%s', '%s', '%d', '%s')" % (
                p_id, title, img_name, price, full_link)
            try:
                cursor.execute(sql)
                cnx.commit()
            except:
                cnx.rollback()

            break


def start_scrapper():
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    subnavs = soup.find_all(class_='subnav')
    for subnav in subnavs:
        subnav = subnavs[8]
        uls = subnav.find_all('ul', class_='flexLabelLinksContainer')
        for ul in uls:
            anchors = ul.select('li a')
            for anchor in anchors:
                partial_url = anchor.get('href')
                if not validators.url(partial_url):
                    link = base_url + anchor.get('href')
                    product_page = requests.get(link)
                    product_soup = BeautifulSoup(product_page.content, 'html.parser')
                    face_container = product_soup.find(id='facet_container')
                    if face_container is not None:
                        # scrapping though product list page
                        scrap_product_page(product_soup)
                    else:
                        print "i am here"
                        subcat = product_soup.find(id='firstNavSubCat')
                        print subcat
                        subcat_lis = subcat.find_all(class_='nav_cat_item_bold')
                        print len(subcat_lis)
        break






start_scrapper()






