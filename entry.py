from typing import Optional
from urllib.request import Request
from fake_useragent import UserAgent
import os

ua = UserAgent()
# BASE_URL = 'https://www.troublecodes.net'
BASE_URL = 'http://localhost:5000'


def createDir(name):
    path = os.getcwd() + '/' + name
    if not os.path.exists(path):
        os.makedirs(path)


headers = {'User-Agent': ua['google chrome']}
req: Optional[Request] = Request(BASE_URL, None, headers)

response = urllib.request.urlopen(req)

responseHeader = response.info()['Content-Type']
statusCode = response.getcode()
print(responseHeader, statusCode)
if statusCode != 200:
    print('http response failed', response)
else:
    data = response.read().decode('utf-8')
    createDir('data')
    text_file = open("data/index.html", "w")
    text_file.write(data)
    text_file.close()
    os.system("python ./parse.py")
