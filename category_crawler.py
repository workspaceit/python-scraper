import urllib2
import json


f = open('cat.json', 'w')

url = "https://api.gilt.com/v1/products/categories.json?apikey=8668a269aded3c5afe896fb815d3a6b31ee09b9b93b5c61ebd504171c9f8cdd2"
req = urllib2.Request(url)
res = urllib2.urlopen(req)
catJsonText = res.read()

cat_json = json.loads(catJsonText)



f.write(json.dumps(cat_json))
f.close()
