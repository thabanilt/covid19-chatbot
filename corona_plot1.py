import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib.styles import LineStyle


def get_data(msg_text,num):
 url = "https://api.covid19api.com/summary"
 

 response = requests.request("GET", url)
 data=response.text
 data=json.loads(data)
 
 for i in range(len(data["Countries"])):
    x=data["Countries"][i]["Country"]
    if(x.lower()==msg_text.lower()):
        total=data["Countries"][i]["TotalConfirmed"]
        recovered=data["Countries"][i]["TotalRecovered"]
        total_deaths=data["Countries"][i]["TotalDeaths"]
        new_deaths=data["Countries"][i]["NewDeaths"]
        data_complete= f'_Covid-19 Cases for *{x}_ \n\nConfirmed Cases : *{total}*  \n\nRecovered : *{recovered}*\n\nDeaths : *{total_deaths}*\n\nNew Deaths : *{new_deaths}* \n\n 👉 Type *Country Name* to check cases  \n 👉 Type *Menu* to view the Main Menu\n\n'
                            
        
        
        return(data_complete)
        break 
     
 return("Country entered not found\n\n👉 Type *Country Name* to check cases  \n 👉 Type *Menu* to view the Main Menu\n\n ")    


