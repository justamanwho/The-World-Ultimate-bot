from bs4 import BeautifulSoup
import urllib.request
import wikipedia
import requests
import json
import os
import re


def get_wiki_links(country):
    wikipedia.set_lang('en')
    page_name = wikipedia.search(country, results=1)
    page = wikipedia.WikipediaPage(page_name)
    page_html = page.html()

    soup = BeautifulSoup(page_html, 'html.parser')

    links = [f'https://en.wikipedia.org' + link['href']
             for link in soup.find_all('a', class_='mw-file-description', limit=4)]

    flag, emblem = links[0], links[1]
    map = links[2] if 'orthographic' in links[2] else links[3]

    underscored_country_name = '_'.join(country.split())
    data = {f'The_Flag_of_{underscored_country_name}': flag, f'The_Coat_Of_Arms_of_{underscored_country_name}': emblem,
            f'The_Map_of_{underscored_country_name}': map}

    return data


def get_wiki_photos_from_links(data):
    link_collection = dict()

    for file_name, link in data.items():
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        parent_div = soup.find('div', {'class': 'fullImageLink', 'id': 'file'})

        if parent_div:
            link = 'https:' + parent_div.find('a')['href']

            link_collection[file_name] = link

    return link_collection


def download_image(country_name, link_collection):
    for file_name, link in link_collection.items():
        directory = f'static/{country_name}'
        os.makedirs(directory, exist_ok=True)

        urllib.request.urlretrieve(link, f'{directory}/{file_name}.svg')


def start_downloading():
    with open('Countries.json', 'r') as file:
        countries = json.load(file)

        for country in countries:
            country_name = country['name']

            data = get_wiki_links(country_name)
            link_collection = get_wiki_photos_from_links(data)

            download_image(country_name, link_collection)


if __name__ == '__main__':
    start_downloading()