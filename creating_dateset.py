import json
import pandas as pd 
import numpy as np

# Opening JSON file
f = open('jsonFile.txt')
  
# returns JSON object as 
# a dictionary

data = json.load(f)
  
# Iterating through the json
# list
df=pd.DataFrame(data)
df_final=df[['game_mode',"players"]]  
# Closing file
f.close()
#print(df_final)
game_mode=df_final.loc[df_final["game_mode"]==22]
print(game_mode)
#print(game_mode["players"].head(5))
dataset=pd.DataFrame()

#Getting all the features
# gold_t,lane_pos,item_0,item_1,item_2,item_3,item_4,item_5,purchase_log=list()
for i in game_mode["players"]:
     #print(i[0]["gold_t"])
     gold_t=i[0]["gold_t"]
     lane_pos=i[0]["lane_pos"]
     item_0=i[0]["item_0"]
     item_1=i[0]["item_1"]
     item_2=i[0]["item_2"]
     item_3=i[0]["item_3"]
     item_4=i[0]["item_4"]
     item_5=i[0]["item_5"]
     hero_id=i[0]["hero_id"]
     item_neutral=i[0]["item_neutral"]
     damage_inflictor=i[0]["damage_inflictor"]
     damage_inflictor_received=i[0]["damage_inflictor_received"]
     purchase_log=i[0]["purchase_log"]
     dicto={"game_mode":22,"gold_t":gold_t,"lane_pos":lane_pos,"item_0":item_0,"item_1":item_1,"item_2":item_2,
            "item_3":item_3,"item_4":item_4,"item_5":item_5,"hero_id":hero_id,"item_neutral":item_neutral,
            "damage_inflictor":damage_inflictor,
            "damage_inflictor_received":damage_inflictor_received,
            "purchase_log":purchase_log}
     #print(dicto)
     
     dataset = dataset.append(dicto,ignore_index=True)

print(dataset)
dataset.to_csv("dataset.csv")
     

