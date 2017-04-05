import mysql.connector
import urllib2
import json
from decimal import Decimal


cnx = mysql.connector.connect(user='root', password='', host='localhost', database='awesome_store')
cursor = cnx.cursor()

api_key = "8668a269aded3c5afe896fb815d3a6b31ee09b9b93b5c61ebd504171c9f8cdd2"
stores = ['women', 'men', 'home']

product_type = {
    'women': 1,
    'men': 2,
    'home': 3
}



with open('cat.json') as json_data:
    cat_json = json.load(json_data)
    categories = cat_json['categories']
    for store in stores:
        store_id = product_type[store]
        for cat in categories:
            print("-----------------Crawling for category: " + cat + "------------------")
            url2 = "https://api.gilt.com/v1/products?q=" + cat + "&store="+ store +"&apikey=" + api_key
            try:
                url2 = url2.replace(" ", "%20")
                req2 = urllib2.Request(url2)
                res2 = urllib2.urlopen(req2)
                search_res_text = res2.read()
                search_json = json.loads(search_res_text)
                total = search_json['total_found']
                products = search_json['products']

                total_request = (total / 100) + 1
                start = 0
                rows = 100
                inserted_item_count = 0
                for i in range(0, total_request):
                    url2 = "https://api.gilt.com/v1/products?q=" + cat + "&store=" + store + "&apikey=" + api_key + "&start=" + str(start) + "&rows=" + str(rows)
                    print(url2)
                    url2 = url2.replace(" ", "%20")
                    try:
                        req2 = urllib2.Request(url2)
                        res2 = urllib2.urlopen(req2)
                        search_res_text2 = res2.read()
                        start += 100
                        search_result_json = json.loads(search_res_text2)
                        search_products = search_result_json['products']

                        print "Sub Category"
                        print url2.string
                        print "Sub Category"

                        for p in search_products:
                            sold_out = p['skus'][0]['inventory_status']
                            # indentedJson = json.dumps(p, indent=4, sort_keys=True)
                            title = p['name']
                            identifier = p['skus'][0]['id']
                            price = 0.0
                            if 'sale_price' in p['skus'][0]:
                                price = p['skus'][0]['sale_price']
                            else:
                                price = p['skus'][0]['msrp_price']
                            image_src = p['image_urls']['300x400'][0]['url']
                            product_url = ""
                            if 'url' in p:
                                product_details_url = p['url']

                            print(title)
                            # print(identifier)
                            # print(price)
                            # print(image_src)
                            # print(product_details_url)



                            sql =   sql = "INSERT INTO products(identifier, title, image, store_id, price, site_id, details_url) VALUES " \
                              "('%s', '%s', '%s', '%d', '%s', '%d', '%s')"  % (identifier, title, image_src, store_id, price, 1, product_details_url)

                            cursor.execute(sql)
                            cnx.commit()
                            inserted_item_count += 1
                    except Exception as e:
                        print e
                        inserted_item_count += 1
                        cnx.rollback()
                        print("Connection refused by the server..")
                        continue

                    if inserted_item_count >= 100:
                        break
            except Exception as e:
                print e
                print("Connection refused by the server..")
                continue
