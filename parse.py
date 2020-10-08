from lxml import etree

html = etree.parse('./data/index.html', etree.HTMLParser())
result = html.xpath('//*')
print(result)
