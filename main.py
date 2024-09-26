import requests
from bs4 import BeautifulSoup

countries = ['Uganda']

for country in countries:
    # Fetch the Wikimedia page HTML
    url = f'https://commons.wikimedia.org/wiki/File:Location{country}.svg'
    response = requests.get(url)

    # Parse the HTML to find the actual file URL
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the link to the SVG file (usually in <a> tag with "original-file-link" class)
    file_link = soup.find('a', {'class': 'internal'})  # "internal" class usually contains the link to the actual file

    if file_link:
        svg_url = file_link['href']  # Get the href and prepend 'https:'
        print(f"Downloading {country} map from: {svg_url}")

        # Download the actual SVG file
        svg_data = requests.get(svg_url)

        # Save the SVG file locally
        with open(f'{country}.svg', 'wb') as file:
            file.write(svg_data.content)
            print(f"{country} map saved as {country}.svg")
    else:
        print(f"Could not find SVG file for {country}.")

# Get all countries



