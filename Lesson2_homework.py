from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
import pandas as pd
import json
import re


ENDPOINT_URL = "https://www.hh.ru/search/vacancy/"
headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36'}
PARAMS = {"page": 1, 'name_of_vacancy':'name', 'items_on_page':'100'}
#time.sleep(N) - N секунд
BS_CLASSES = {
    "elements": re.compile("styles_content__.*"),
    "name": re.compile("styles_mainTitle__.*"),
    "original_name": re.compile("desktop-list-main-info_secondaryText__.*"),
    "rating": re.compile(".*styles_kinopoiskValue__.*"),
}

class Vacancy_searcher:
    def __init__(self, start_url, params, headers):
        self.headers = headers
        self.start_url = start_url
        self.start_params = params
        self.info_about_vacancy = []

    def get_html_string(self, url, params):
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            time.sleep(1)
            print(e)
            return None
        return response.text

    def get_dom(html_string):
        return BeautifulSoup(html_string, "html.parser")

    def run(self):
        self.paginate(self.start_url, self.start_params)
        # or get it from the page?
        for page_number in range(2, 5):
            params = self.start_params
            params["page"] = page_number
            self.paginate(self.start_url, params)

    def extract_text(self, element, cls):
        return element.find(attrs={"class": BS_CLASSES[cls]}).text

    def get_info_from_element(self, element):
        vacancy_info = []
        info = {}
        info["name"] = self.extract_text(element, "resume-search-item__name")
        info["company_name"] = self.extract_text(element, "vacancy-serp-item__meta-info")
        info["city"] = self.extract_text(element, "vacancy-serp-item__meta-info")
        info["salary"] = self.extract_text(element, "vacancy-serp-item__compensation")
        if not info["salary"]:
            salary_min = None
            salary_max =None
            salary_currency = None
        else:
            salary = float(info["salary"])
            salary = re.split(r'\s|-', salary)
            if salary[0]== 'до':
                salary_min = None
                salary_max =int(salary[1])
            elif salary[0]=='от':
                salary_min = int(salary[1])
                salary_max = None
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[1])
            salary_currency = salary[2]
        info["salary_min"] = salary_min
        info["salary_max"] = salary_max
        info["salary_currency"] = salary_currency
        info["vacancy_link"] = self.extract_text(element, "vacancy-serp-item__controls-item vacancy-serp-item__controls-item-last")
        info["vacancy_link"] = info["vacancy_link"].find('a')['href']
        vacancy_info.append(info)
        return vacancy_info

        with open('hh.json', 'w') as ht:
            json.dump(vacancy_info, ht)

    def paginate(self, url, params):
        html_string = self.get_html_string(url, params)
        if html_string is None:
            print("There was an error")
            return

        soup = Vacancy_searcher.get_dom(html_string)
        vacancy_elements = list(
            map(
                lambda x: x.parent,
                soup.find_all("div", attrs={"class": BS_CLASSES["elements"]}),
            )
        )
        for element in vacancy_elements:
            info = self.get_info_from_element(element)
            self.info_about_vacancy.append(info)



if __name__ == "__main__":
    scraper = Vacancy_searcher(ENDPOINT_URL, PARAMS, headers)
    scraper.run()


