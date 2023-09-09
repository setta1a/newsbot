import requests
from bs4 import BeautifulSoup


def get_news(link):
    link_href = link.get("href")
    curr_url = 'https://www.rg.ru/' + link_href
    response = requests.get(curr_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find('div', class_='PageArticleContent_lead__gvX5C').text


def get_latest_updates_main():
    updates = []

    url = 'https://www.rg.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headers = soup.find('span', class_='ItemOfListStandard_title__eX0Jw')
    link = soup.find("a", class_="ItemOfListStandard_imageLinkBox__wi4cV")
    imgs = soup.find("img", class_="Image_img__m9RSC ItemOfListStandard_image___sWCo")
    updates.append(
        {"Заголовок": headers.text, "Описание": get_news(link), "Картинка": imgs.get('src', None)})

    return updates


def get_latest_updates_news():
    curr_url = 'https://www.rg.ru/news.html'
    response = requests.get(curr_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find("span", class_="ItemOfListStandard_title__eX0Jw").text
    link_element = soup.find("a", class_="ItemOfListStandard_datetime__1tmwG")

    updates = []

    if link_element:
        link = link_element.get("href")

        URL = f"https://www.rg.ru{link}"
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        lead = soup.find("h1", class_="PageArticleContent_title__RVnvC").text
        ling = (soup.find("div", class_="PageContentCommonStyling_text__fCZrl").text + "\n"
                + soup.find('div', class_='PageArticleContent_lead__gvX5C').text)
        photo = soup.find("img", class_="Image_img__m9RSC undefined")
        photo_src = None
        if photo:
            photo_src = photo.get('src', None)

        updates.append(
            {"Дата": link_element.text, "Заголовок": lead, "Описание": ling, "Картинка": photo_src})

        return updates

    else:
        print("Ошибка")