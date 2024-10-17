# Making file with all of not sovereign countries
with open('data/the-world.txt', 'r', encoding='utf-8') as all_countries:
    with open('data/sovereign-countries.txt', 'r', encoding='utf-8') as sovereign_countries:
        with open('data/not-sovereign-countries.txt', 'w', encoding='utf-8') as keeper:
            all_countries = [line.strip() for line in all_countries.readlines()]
            sovereign_countries = [line.strip() for line in sovereign_countries.readlines()]

            for country in all_countries:
                if country not in sovereign_countries:
                    keeper.write(country+'\n')
