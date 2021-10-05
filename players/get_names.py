import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json

# setup emtpy list for later player names
player_list = []

# generate ids for thesportsdb api
player_ids = np.arange(start=34145352, stop=34145370, step=1)

# create url and send request
for i in player_ids:
    url = f"https://www.thesportsdb.com/api/v1/json/1/lookupplayer.php?id={i}"

    response_object = requests.get(url)
    response_data = response_object.json()

    if response_data.get("players") is None:
        continue

    playername = response_data.get("players")[0]["strPlayer"]
    player_list.append(playername)

    


