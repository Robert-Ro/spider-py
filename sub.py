import urllib.request
import redis 
from fake_useragent import UserAgent
import os
ua = UserAgent()

BASE_URL = 'http://localhost:5000' 
def createDir(name):
    path = os.getcwd()+'/' + name
    if not os.path.exists(path):
        os.makedirs(path)

redisInstance = redis.Redis(host='localhost', port=6379, db=0)
 
redisPub = redisInstance.pubsub()
redisPub.psubscribe('url-add-channel')

def crawl(url):
    # 爬取内容: 1.控制速度
    headers = {'User-Agent': ua['google chrome']} 
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    # content-type为text/html时，存储的同时调用parse去解析它
    if response.getcode()!= 200:
        print('something error', response.geturl())
    contentType = response.info()["content-type"]
    data = response.read().decode('utf-8')
    dir = 'temp' 
    
    dirs = url.replace(BASE_URL, '').split('/')
    if dirs[-1]: 
        last = dirs.pop()
        dir = 'temp'+'/'.join(dirs)
        filename = last.split('.')[0]
    else:  
        filename = 'index' 
    createDir(dir)
    if  'html' in contentType:
        text_file = open(dir+"/"+ filename +".html", "w")  
    elif 'css' in contentType: 
        text_file = open(dir+"/"+ filename+".css", "w")    
    elif 'jpeg' in contentType: 
        text_file = open(dir+"/"+ filename+".jpeg", "w")    
    elif 'javascript' in contentType: 
        text_file = open(dir+"/"+ filename+".js", "w")    
    else:
        pass
    text_file.write(data)
    # todo 更新url
    redisInstance.set('status_['+BASE_URL+url+']', 1)
    text_file.close()

while True:
    # {'type': 'pmessage', 'pattern': b'url-add-channel', 'channel': b'url-add-channel', 'data': b'https://www.troublecodes.net/ford'} 
    message =  redisPub.get_message()
    if message!= None and message['type'] == 'pmessage': 
        print('get message', message)
        crawl(message['data'])
        # 加入到redis队列中，通过设置传入参数，爬取完毕后，更新字段是否被爬取

