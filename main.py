import requests
from bs4 import BeautifulSoup
import wikipedia
import re


def get_wiki_image(country_name):
    wikipedia.set_lang('en')
    page_name = wikipedia.search(country_name)[0]
    page = wikipedia.WikipediaPage(page_name)
    page_html = page.html()

    soup = BeautifulSoup(page_html, 'html.parser')

    # underscored_country_name = '_'.join(country_name.split())

    # # Flag
    # flag_href_pattern = fr'/wiki/File:Flag_of_{underscored_country_name}.svg'
    # flag_title_pattern = fr'Flag of {country_name}'
    # flag_link = 'https://en.wikipedia.org' + soup.find('a', href=re.compile(flag_href_pattern),
    #                                                    title=re.compile(flag_title_pattern), class_='mw-file-description')['href']
    #
    # # Emblem
    # emblem_href_pattern = fr'/wiki/File:(Emblem|Coat_of_arms)_of_{underscored_country_name}.svg'
    # emblem_title_pattern = fr'(Emblem|Coat of arms) of {country_name}'
    # emblem_link = 'https://en.wikipedia.org' + soup.find('a', href=re.compile(emblem_href_pattern),
    #                                                      title=re.compile(emblem_title_pattern), class_='mw-file-description')['href']
    #
    # # Map
    # map_href_pattern = f'/wiki/File:{underscored_country_name}_(orthographic_projection).svg'
    # map_link = 'https://en.wikipedia.org' + soup.find('a', href=map_href_pattern, class_='mw-file-description')['href']

    links = soup.find_all('a', class_='mw-file-description')

    flag_link, emblem_link = links[0]['href'], links[1]['href']
    map_link = links[2]['href'] if country.split()[0] in links[2]['href'] else links[3]['href']

    return flag_link, emblem_link, map_link



for country in ['China', 'Taiwan', 'Japan']:
    print(country)
    file_url = get_wiki_image(country)
    print(file_url)
