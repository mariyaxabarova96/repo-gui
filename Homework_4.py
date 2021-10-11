from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('127.0.0.1', 27017)
db = client['News']
news_item = db.news
url = 'https://yandex.ru/news'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
    }
response = requests.get(url, headers = headers)
dom = html.fromstring(response.text)
items = dom.xpath("//article[contains(@class, 'mg-card')]")


for i in items:
    news = {}
    title = i.xpath(".//h2[@class = 'mg-card__title']/text()")
    title = str(title).replace("\\xa0", " ")
    link = i.xpath(".//a[@class = 'mg-card__link']/@href")
    date = i.xpath(".//span[@class='mg-card-source__time']/text()")
    source = i.xpath(".//a[@class='mg-card__source-link']/text()")
    news['title'] = title
    news['link'] = link
    news['date'] = date
    news['source'] = source
    pprint(news)
    try:
        news_item.update_one({'link':news['link']}, {'$set': news}, upset = True)
    except Exception as exc:
        pprint ('haha')
        continue