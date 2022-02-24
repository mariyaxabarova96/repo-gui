from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
client = MongoClient('127.0.0.1',27017)
database = client['news']

def news_mail():
    news_list_mail= []
    url = 'https://news.mail.ru/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_elements = dom.xpath("//ul[@data-module='TrackBlocks']/li[@class='list__item']")
    for element in news_elements:
        news = {
            'title': str(element.xpath(".//text()")).replace("\\xa0", " "),
            'url': str(element.xpath("./a/@href")),
            'source': str(dom.xpath("./a[contains(@class, 'link color_gray breadcrumbs__link')]/span/text()")),
            'date': str(element.xpath("//span[@datetime]/@datetime")[0])
                }
        news_list_mail.append(news)
    #pprint(news_list_mail)
    return news_list_mail

def news_lenta():
    news_list_lenta = []
    url = 'https://lenta.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_elements = dom.xpath("//section[contains(@class,'main-page__section')]//a[@class='card-mini _topnews']")
    for element in news_elements:
        news = {
            'title': str(element.xpath("./div[contains(@class,'card-mini__text')]/span/text()")),
                'url':  url + str(element.xpath("./@href")[0]),
                'source': 'Lenta.RU',
                'publication_date': str(element.xpath("//div[contains(@class,'card-mini__info')]//time/text()")[0])
             }
        news_list_lenta.append(news)
    #pprint(news_list_lenta)
    return news_list_lenta



def news_yandex():
    news_list_yandex = []
    url = 'https://yandex.ru/news'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_elements = dom.xpath("//div[contains(@class,'mg-grid__col mg-grid__col_xs_4')]")#mg-grid__col_sm_9')]")

    for element in news_elements:
        news = {
            'title': str(element.xpath(".//div[contains(@class, 'mg-card__annotation')]/text()")).replace("\\xa0", " "),
            # 'title': str(element.xpath(".//h2/a/text()")[0]).replace("\\xa0", " "),
            'url': str(element.xpath(".//h2/a/@href")),
                #'url':  str(element.xpath(".//h2/a/@href")),
                #'source': str(element.xpath(".//span[@class='mg-card-source__source']/a/text()")),
            'source': str(element.xpath(".//span[contains(@class, 'mg-card-source__source')]/a/text()")),
            'publication_date': str(element.xpath(".//span[@class='mg-card-source__time']/text()"))
            }
        news_list_yandex.append(news)
    #pprint(news_list_yandex)
    return news_list_yandex





news_result = news_mail()
news_result += news_lenta()
news_result += news_yandex()

database.news.insert_many(news_result)
pprint(news_result)
