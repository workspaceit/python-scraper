import urllib2
import json

#url = "https://api.gilt.com/v1/products/categories.json?apikey=8668a269aded3c5afe896fb815d3a6b31ee09b9b93b5c61ebd504171c9f8cdd2"
#req = urllib2.Request(url)
#res = urllib2.urlopen(req)
# catJsonText = res.read()

with open('categories2.json') as json_data:
    cat_json = json.load(json_data)
    categories = cat_json['categories']
    f = open('out2.json', 'a')
    for cat in categories:
        print("-----------------Crawling for category: " + cat + "------------------")
        url2 = "https://api.gilt.com/v1/products?q=" + cat + "&apikey=8668a269aded3c5afe896fb815d3a6b31ee09b9b93b5c61ebd504171c9f8cdd2"
        url2 = url2.replace(" ", "%20")
        # print(url2)
        req2 = urllib2.Request(url2)
        res2 = urllib2.urlopen(req2)
        search_res_text = res2.read()
        search_json = json.loads(search_res_text)
        total = search_json['total_found']
        products = search_json['products']

        total_request = (total / 100) + 1
        start = 0
        rows = 100
        for i in range(0, total_request):
            url2 = "https://api.gilt.com/v1/products?q=" + cat + "&apikey=8668a269aded3c5afe896fb815d3a6b31ee09b9b93b5c61ebd504171c9f8cdd2&start=" + str(start) + "&rows=" + str(rows)
            print(url2)
            url2 = url2.replace(" ", "%20")
            req2 = urllib2.Request(url2)
            res2 = urllib2.urlopen(req2)
            search_res_text2 = res2.read()
            start += 100
            search_result_json = json.loads(search_res_text2)
            search_products = search_result_json['products']
            for p in search_products:
                # indentedJson = json.dumps(p, indent=4, sort_keys=True)
                f.write(json.dumps(p) + ',\n')
    f.close()

