from bs4 import BeautifulSoup
import urllib.request
import requests
import logging
import json
import os


def get_wiki_links(country):
    page_name = f'https://en.wikipedia.org/wiki/{country}'
    page_html = requests.get(page_name).text
    soup = BeautifulSoup(page_html, 'html.parser')

    anchor_elements = [link for link in soup.find_all('a', class_='mw-file-description', limit=4)]
    links = [f'https://en.wikipedia.org' + link['href'] for link in anchor_elements]

    flag, emblem = links[0], links[1]

    underscored_country_name = '_'.join(country.split())
    data = {f'The_Flag_of_{underscored_country_name}': flag, f'The_Coat_of_Arms_of_{underscored_country_name}': emblem}

    # key_map_words = ('location', 'orthographic', 'map', 'earth', 'world')

    # If the Country has A Seal of State, then it's added. Otherwise, it's just the map
    undefined = str(anchor_elements[2]).lower()
    if 'seal' in undefined:
        data[f'The_Seal_of_State_of_{underscored_country_name}'] = links[2]
        data[f'The_Map_of_{underscored_country_name}'] = links[3]
    else:
        data[f'The_Map_of_{underscored_country_name}'] = links[2]

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
        try:
            directory = f'static/{country_name}'
            os.makedirs(directory, exist_ok=True)

            extention = link.split(".")[-1]
            file_path = f'{directory}/{file_name}.{extention}'
            urllib.request.urlretrieve(link, file_path)

            logger.info(f'Completed downloading of {file_path} with link {link}')
        except Exception:
            logger.error(f"Wasn't able to download {file_name} with link {link}")


def start_downloading():
    with open('data/all_countries.json', 'r', encoding='utf-8') as file:
        countries = json.load(file)

        for country in countries:
            country_name = country['name']
            logger.info(f'Start downloading {country_name}')

            data = get_wiki_links(country_name)
            link_collection = get_wiki_photos_from_links(data)

            download_image(country_name, link_collection)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s | %(name)s | %(asctime)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    file_handler = logging.FileHandler(f'{logger.name}.log')
    logger.addHandler(file_handler)

    start_downloading()
