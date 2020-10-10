from lxml import etree
import redis

html = etree.parse('./data/index.html', etree.HTMLParser())
result = html.xpath('//*')
r = redis.Redis(host='localhost', port=6379, db=0)
res = r.get('test')
print(res)
# TODO
# 1. get all link to save redis
# 2. fork child-process or use thread to crawl
