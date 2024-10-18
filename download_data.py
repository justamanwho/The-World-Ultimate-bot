from bs4 import BeautifulSoup
import urllib.request
import wikipedia
import requests
import os
import logging.config


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('Downloading')


def get_wiki_links(country, page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    anchor_elements = [link for link in soup.find_all('a', class_='mw-file-description', limit=4)]
    links = [f'https://en.wikipedia.org' + link['href'] for link in anchor_elements]

    flag, emblem = links[0], links[1]

    underscored_country_name = '_'.join(country.split())
    files_data = {f'The_Flag_of_{underscored_country_name}': flag, f'The_Coat_of_Arms_of_{underscored_country_name}': emblem}

    # key_map_words = ('location', 'orthographic', 'map', 'earth', 'world')

    # If the Country has A Seal of State, then it's added. Otherwise, it's just the map
    undefined = str(anchor_elements[2]).lower()
    if 'seal' in undefined:
        files_data[f'The_Seal_of_State_of_{underscored_country_name}'] = links[2]
        files_data[f'The_Map_of_{underscored_country_name}'] = links[3]
    else:
        files_data[f'The_Map_of_{underscored_country_name}'] = links[2]

    return files_data


def get_wiki_photos_from_links(files_data):
    link_collection = dict()

    for file_name, link in files_data.items():
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        parent_div = soup.find('div', {'class': 'fullImageLink', 'id': 'file'})

        if parent_div:
            link = 'https:' + parent_div.find('a')['href']
            link_collection[file_name] = link

    return link_collection


def download_images(country_name, link_collection):
    for file_name, link in link_collection.items():
        try:
            directory = f'static/{country_name}'
            os.makedirs(directory, exist_ok=True)

            extension = link.split(".")[-1]
            file_name_extension = f'{file_name}.{extension}'

            file_path = f'{directory}/{file_name_extension}'
            urllib.request.urlretrieve(link, file_path)

            logger.info(f'Completed downloading of {file_name_extension} with link {link}')
        except Exception:
            logger.error(f"Wasn't able to download {file_name} with link {link}")


def download_text_info(summary, country_name):
    underscored_country_name = '_'.join(country_name.split())
    text_data = {f'Summary_of_{underscored_country_name}.txt': summary}

    for text_file, content in text_data.items():
        with open(f'static/{country_name}/{text_file}', 'w', encoding='utf-8') as file:
            file.write(content)

            logger.info(f'Completed downloading of {text_file}')


def start_downloading():
    with open('data/the-world.txt', 'r', encoding='utf-8') as file:
        countries = [line.strip() for line in file.readlines()]

        for country in countries:
            logger.info(f'Start downloading {country}')

            # Set up Wikipedia environment
            wikipedia.set_lang('en')
            page_name = wikipedia.search(country)[0]
            page = wikipedia.WikipediaPage(page_name)
            page_html = page.html()

            # Download images data
            data = get_wiki_links(country, page_html)
            link_collection = get_wiki_photos_from_links(data)
            download_images(country, link_collection)

            # Download text data
            page_summary = page.summary.split('.')[1]
            download_text_info(page_summary, country)


if __name__ == '__main__':
    start_downloading()
