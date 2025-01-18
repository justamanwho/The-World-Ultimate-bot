# Input: 
- Country name

# Output: 
- Coat of Arms (photo)
- Map (photo)
- Flag (photo)
- Seal (photo)
- Capital
- Summary
- Area in km^2
- Population
- GDP
- Currency


# Notes:
- Originally country names are from https://stefangabos.github.io/world_countries/ (What needs to be checked to download data: (English->Countries->JSON))
- Then I changed them a little so the Wikipedia API could recognize it.
- Telegram Bot doesn't support sending the svg files :( , so I converted all the media to png.


# To do list:
- Send 'the-world-map' picture when someone types 'The World'
- Change the similarity search module, since this one sucks.
