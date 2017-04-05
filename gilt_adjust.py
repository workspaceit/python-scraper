import json

with open('home.json') as json_data:
    products = json.load(json_data)
    pros = []
    f = open('home_gilt.json', 'w')
    for pro in products:
        pros.append({
            'desc': pro['name'],
            'brand': pro['brand'],
            'prices': [ pro['skus'][0]['msrp_price'], pro['skus'][0]['sale_price'] ],
            'img': pro['image_urls']['300x400'][0]['url']
        })
    for p in pros:
        f.write(json.dumps(p) + ',\n')
    f.close()

