import re

import redis
from lxml import etree

redisInstance = redis.Redis(host='localhost', port=6379, db=0)
# BASE_URL = 'https://www.troublecodes.net'
# re1 = r"https:\/\/www.troublecodes.net"
# re2 = r"https:\/\/www.troublecodes.net\/?$"

BASE_URL = 'http://localhost:5000'
re1 = r"http:\/\/localhost:5000"
re2 = r"http:\/\/localhost:5000\/?$"

html = etree.parse('./data/index.html', etree.HTMLParser())

# 获取所有的a标签，筛选非本protocol的元素： 1.存储路径待爬取


def getValidLinkElement(ele):
    href = ele.get('href')
    if href == "/":
        return False
    if bool(re.match("http", href)):
        if bool(re.match(re1, href)):
            a = bool(re.match(re2, href))
            return not a
        else:
            return False

    return True


def getValidHref():
    # 本地资源
    #

    results = html.xpath('//a')

    filterResults = filter(getValidLinkElement, results)
    validUrls = []
    for ele in filterResults:
        href = ele.get('href')
        print(href)
        if bool(re.match(re1, href)):
            validUrls.append(href.split('#')[0])
        else:
            if '#' in href:
                if href.split('#')[0] != '':
                    validUrls.append(BASE_URL + href.split('#')[0])
            else:
                validUrls.append(BASE_URL + href)
    return validUrls


def getValidLinks():
    stylesheets = html.xpath('//link[@rel="stylesheet"]')
    urls = []
    for ele in stylesheets:
        href: str = ele.get('href')

        ele.set('href', '')  # TODO 替换成本地资源
        if bool(re.match(re1, href)):
            urls.append(href)
        else:
            urls.append(BASE_URL + href)
    scripts = html.xpath('//script[@src!=""]')
    for ele in scripts:
        src = ele.get('src')
        if bool(re.match(re1, src)):
            urls.append(src)
        else:
            urls.append(BASE_URL + src)
    imgs = html.xpath('//img[@src!=""]')
    for ele in imgs:
        src = ele.get('src')
        if bool(re.match(re1, src)):
            urls.append(src)
        else:
            urls.append(BASE_URL + src)
    return urls


# 获取所有的link rel=icon/apple-touch-icon/stylesheet
# 获取所有的script
# 获取所有的img
# 替换链接

# TODO
# 1. get all link to save redis
# 2. 发布订阅
# 2. fork child-process or use thread to crawl

urls = list(set(getValidHref()))
urls2 = getValidLinks()
for url in urls + urls2:
    if not redisInstance.sismember("crawl_urls", url):
        print(url, 'sadd')
        redisInstance.sadd("crawl_urls", url)
        redisInstance.set('status_[' + url + ']', 0)
        redisInstance.publish('url-add-channel', url)
