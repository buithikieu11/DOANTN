import requests
from time import sleep

from tqdm import tqdm
import pymongo
from pymongo import MongoClient
import logging
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO
fmt_url = 'https://api.viblo.asia/posts?page={}'

client = MongoClient(port=27017)
db=client.rsblog
col=db.viblo_posts

col.count()
page = 1
count = 0
while True:
    try:
        req = requests.get(fmt_url.format(page))
        if req.status_code != 200:
            break
        if page == 500:
            print('stop')
            break
        data = req.json()['data']
        for post in data:
            col.insert_one({
                'id': post['id'] ,
                'title': post['title'],
                'slug': post['slug'],
                'url': post['url'],
                'content': post['contents'],
                'reading_time': post['reading_time'],
            })
    
        page += 1
        sleep(0.1)
        
        if page % 50 == 0:
            print(col.count())
    except Exception as e:
        print(e)
        continue
