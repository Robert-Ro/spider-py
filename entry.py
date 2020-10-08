import urllib.request
from fake_useragent import UserAgent
import os

ua = UserAgent()


def createDir(name):
    path = os.getcwd()+'/' + name
    if not os.path.exists(path):
        os.mkdir(path)


user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

headers = {'User-Agent': ua['google chrome']}
# headers = {
#     'User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
req = urllib.request.Request('https://www.troublecodes.net', None, headers)
response = urllib.request.urlopen(req)
data = response.read().decode('utf-8')
# multi-thread

createDir('data')
text_file = open("data/index.html", "w")
text_file.write(data)
text_file.close()
