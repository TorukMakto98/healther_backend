import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
To make the request to the page we have to inform the
website that we are a browser and that is why we
use the headers variable
"""
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# endereco_da_pagina stands for the data page address
url = "https://www.transfermarkt.co.uk/ajax-amsterdam/transferrekorde/verein/610/saison_id//pos//detailpos/0/w_s//altersklasse//plus/1"

# In the objeto_response variable we will the download of the web page
response_object = requests.get(url, headers=headers)

"""
Now we will create a BeautifulSoup object from our object_response.
The 'html.parser' parameter represents which parser we will use when creating our object,
a parser is a software responsible for converting an entry to a data structure.
"""
page_bs = BeautifulSoup(response_object.content, 'html.parser')

player_names= [] # List that will receive all the players names

# The find_all () method is able to return all tags that meet restrictions within parentheses
player_tags = page_bs.find_all("a", {"class": "spielprofil_tooltip"})
# In our case, we are finding all anchors with the class "spielprofil_tooltip"

# Now we will get only the names of all players
for i in player_tags:
    player_names.append(i.text)

player_list = [] # List that will receive all the names of the countries of the players’s previous leagues.

league_tag = page_bs.find_all("td", {"class": None})
# Now we will receive all the cells in the table that have no class atribute set

for j in league_tag:
    # The find() function will find the first image whose class is "flaggenrahmen" and has a title
    nation_flag = j.find("img", {"class": "flaggenrahmen"}, {"title":True})
    # The country_image variable will be a structure with all the image information,
    # one of them is the title that contains the name of the country of the flag image
    if(nation_flag != None): # We will test if we have found any matches than add them
        player_list.append(nation_flag['title'])

player_costs_list = []

price_tag = page_bs.find_all("td", {"class": "rechts hauptlink"})

for p in price_tag:
    price_text = p.text
    # The price text contains characters that we don’t need like £ (euros) and m (million) so we’ll remove them
    price_text = price_text.replace("£", "").replace("m", "")
    # We will now convert the value to a numeric variable (float)
    player_nr = float(price_text)
    player_costs_list.append(player_nr)

# Creating a DataFrame with our data
df = pd.DataFrame({"Jogador":player_names,"Preço (milhão de euro)":player_costs_list, "País de Origem":player_list})

# Printing our gathered data
print(df)
print(page_bs)