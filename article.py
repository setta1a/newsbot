import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, link):
        self.link = link
        self.image = None

    def get_info(self):
        url = "https://rg.ru" + self.link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.header = soup.find("h1", class_="PageArticleContent_title__RVnvC")
        self.text = ""
        if self.header:
            self.header = self.header.text
            self.text = (soup.find("div", class_="PageContentCommonStyling_text__fCZrl").text + "\n"
                         + soup.find('div', class_='PageArticleContent_lead__gvX5C').text)

    def get_main_info(self):
        url = "https://rg.ru" + self.link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.header = soup.find("h1", class_="PageArticleContent_title__RVnvC")
        self.text = ""
        if self.header:
            self.header = self.header.text
            self.text = (soup.find("div", class_="PageContentCommonStyling_text__fCZrl").text)
            self.image = soup.find('img', class_='RgPhotoreportClassic_mainImg__TSVtW')

    def print(self):
        print(self.header, "; ", self.text)
