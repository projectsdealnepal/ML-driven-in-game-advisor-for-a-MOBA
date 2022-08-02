from turtle import clear
import requests
import Constant
import json
import pandas as pd
import numpy as np  
from time import time, sleep
custom_header = {"Authorization": "Bearer" + Constant.API_KEY}
url="https://api.opendota.com/api/parsedMatches"
r = requests.get(url, headers = custom_header)
matches_id = r.content
y=json.loads(matches_id)
match_id=[d['match_id'] for d in y]
for i in range(0, len(match_id)):
    match_id[i] = int(match_id[i])

for i in match_id:
        print(i)
        sleep(5)
        url1="https://api.opendota.com/api/matches/{}".format(i)
        r = requests.get(url1, headers = custom_header)
        y=json.loads(r.content)
        #jsn.extend(y)
        with open('jsonFile.txt', "a") as convert_file:
            convert_file.write (json.dumps(y))
            convert_file.write(",")
    #  print(y.keys())
    #  print(y["players"])
     #check=[d for d in y["players"] if y["game_mode"]==22]
     #player.extend(check)
     
#print(player)
#6688704217

