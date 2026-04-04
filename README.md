# The World telegram bot
A simple bot that fetches and displays key information about any country. Enter a country name, and the bot returns a complete overview including visual elements (coat of arms, map, flag, seal) and essential statistics (capital, population, area, GDP, currency).


## Input: 
- Country name


## Output: 
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


## Notes:
- Originally country names are from https://stefangabos.github.io/world_countries/ (What needs to be checked to download data: (English->Countries->JSON))
- Then I changed them a little so the Wikipedia API could recognize it.
- Telegram Bot doesn't support sending the svg files :( , so I converted all the media to png.


## Links and Sources:
- telegram bot - https://t.me/The_World_ultimate_bot

<img width="386" height="1012" alt="The-World-bot" src="https://github.com/user-attachments/assets/b9f3660a-1d84-4f66-b2ee-ab1954431a7c" />


## To do list:
- Every continent with country names on it, so the user can write 'Europe' and see the countries he can type in.
