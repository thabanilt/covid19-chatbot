#tutorial5
#whatsapp bot to get live status update on corona virus
import csv
from pymongo import MongoClient
from flask import Flask ,request
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import urllib
import requests
import json
from corona_plot1 import get_data
from corona_news import get_news
import os



client=MongoClient("mongodb://lex:warumwa@cluster0-shard-00-00-lct7x.mongodb.net:27017,cluster0-shard-00-01-lct7x.mongodb.net:27017,cluster0-shard-00-02-lct7x.mongodb.net:27017/corona?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db=client["corona"]
collection=db["corona"]
collections=db["report"]

apbot=Flask(__name__)
fullname=""
@apbot.route("/")
def hpme():
    return "hie"

@apbot.route("/sms",methods=["get","post"])
def reply():
    num=request.form.get("From")
    num=num.replace("whatsapp:","") 
    msg_text=request.form.get("Body")
    lat=request.form.get("Latitude")
    lng=request.form.get("Longitude")
    
    med = request.values.get('MediaContentType0', '')
    x=collection.find_one({"NUMBER":num})
    try:
        status=x["status"]
    except:
        pass
        
    if(bool(x)==False):   
     collection.insert_one({"NUMBER":num,"status":"first"})
     msg=MessagingResponse()
     resp=msg.message("Hello 🙋🏽‍♂, \nIm Lento, Im to provide latest information updates i.e cases in different countries and create awareness to help you and your family stay safe.\n For any emergency 👇 \n 📞 Toll-Free Number: 2 0 1 9 \n\n Please enter one of the following option 👇 \n *A*. Covid-19 statistics *Worldwide*. \n *B*. Covid-19 Statistics in *countries*. \n *C*. Covid-19 News *Worldwide_*. \n *D*. How does it *Spread*? \n *E*. *Preventive measures* to be taken.\n\n*F*. *Report if you Suspect you have covid-19 virus🚑*\n\n*Please be adviced this is a test run.*")
     return(str(msg))



     
    elif (status=="first") :
            msg=MessagingResponse()
            if(msg_text.lower()=="b"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"second"}})
                resp=msg.message("Enter the name of the country for example Zimbabwe\n\n*Please be adviced this is a test run.*")

                return(str(msg))

            elif(msg_text.lower()=="a"):
                  
                  r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
                  if r.status_code == 200:
                    data = r.json()
                    text = f'_Covid-19 Cases Worldwide_ \n\nConfirmed Cases : *{data["cases"]}* \n\nDeaths : *{data["deaths"]}* \n\nRecovered : *{data["recovered"]}* \n\n 👉 Type *B, C, D, E,F* to see other options \n 👉 Type *Menu* to view the Main Menu\n\n*'
                    resp=msg.message(text)
                    print(text)
                    return(str(msg)) 
            elif(msg_text.lower()=="c"):
                  r = requests.get('http://newsapi.org/v2/everything?q=covid19&from=2020-04-09&sortBy=popularity&apiKey=426e591a64e44124bb388e53ef227ff1')
                  if r.status_code == 200:
                    data = r.json()
                    lut=[]
                    text = f'_Covid-19 News Worldwide_\n\n'
                    resp1=msg.message(text)
                    for val in data["articles"]:
                         answ = f'*{val["title"]}* \n\n*{val["description"]}* \n\n*{val["content"]}*\n\n *{val["url"]}*\n\n 👉 Type *A,B, D, E,F* to see other options \n 👉 Type *Menu* to view the Main Menu\n\n'
                         lut=answ
                         resp=msg.message(answ)
                    return(str(msg)) 
                
                  return(str(msg))
            elif(msg_text.lower()=="d"):
                   resp1=msg.message("") 
                   text = f'_Coronavirus spreads from an infected person through_ 👇 \n\n ♦ Small droplets from the nose or mouth which are spread when a person coughs or sneezes \n\n ♦ Touching an object or surface with these droplets on it and then touching your mouth, nose, or eyes before washing your hands \n \n ♦ Close personal contact, such as touching or shaking hands \n Please watch the video for more information 👇 https://youtu.be/TjcoN9Aek24 \n\n👉 Type *A,B, C,E,* to see other options \n  👉 Type *Menu* to view the Main Menu\n\n'
                   resp1.media('https://user-images.githubusercontent.com/34777376/77290801-f2421280-6d02-11ea-8b08-fdb516af3d5a.jpeg')
                   resp=msg.message(text)

                   return(str(msg))
            elif(msg_text.lower()=="e"):
                   resp1=msg.message("") 
                   text = f'_Coronavirus infection can be prevented through the following means_ 👇  \n ✔️ Clean hand with soap and water or alcohol-based hand rub \n https://youtu.be/EJbjyo2xa2o \n\n ✔️ Cover nose and mouth when coughing & sneezing with a tissue or flexed elbow \n https://youtu.be/f2b_hgncFi4 \n\n ✔️ Avoid close contact & maintain 1-meter distance with anyone who is coughing or sneezin \n https://youtu.be/mYyNQZ6IdRk \n\n ✔️ Isolation of persons traveling from affected countries or places for at least 14 day \n https://www.mohfw.gov.in/AdditionalTravelAdvisory1homeisolation.pdf \n\n ✔️ Quarantine if advise \n https://www.mohfw.gov.in/Guidelinesforhomequarantine.pdf \n\n 👉 Type *A,B, C, D, * to see other options \n  👉 Type *Menu* to view the Main Menu\n\n'
                   resp1.media('https://user-images.githubusercontent.com/34777376/77290864-1c93d000-6d03-11ea-96fe-18298535d125.jpeg')
                   resp=msg.message(text)
                   return(str(msg))
            elif(msg_text.lower()=="f"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"report"}})
                resp=msg.message("Enter your name and surname\n\n")
                return(str(msg))
            elif(msg_text.lower()=="menu"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
                msg=MessagingResponse()
                resp=msg.message("Hello 🙋🏽‍♂, \nIm Lento, Im to provide latest information updates i.e cases in different countries and create awareness to help you and your family stay safe.\n For any emergency 👇 \n 📞 Toll-Free Number: 2 0 1 9 \n\n Please enter one of the following option 👇 \n *A*. Covid-19 statistics *Worldwide*. \n *B*. Covid-19 Statistics in *countries*. \n *C*. Covid-19 News *Worldwide_*. \n *D*. How does it *Spread*? \n *E*. *Preventive measures* to be taken.\n\n*F*. *Report if you Suspect you have covid-19 virus🚑*\n\n*Please be adviced this is a test run.*")
                return(str(msg))
            else: 
               resp=msg.message("Invalid input please try again\n\n")
                
               return(str(msg))
    else :
        
        if (status=="second"):
            if (msg_text.lower()=="menu"):
                collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
                msg=MessagingResponse()
                resp=msg.message("Hello 🙋🏽‍♂, \nIm Lento, Im to provide latest information updates i.e cases in different countries and create awareness to help you and your family stay safe.\n For any emergency 👇 \n 📞 Toll-Free Number: 2 0 1 9 \n\n Please enter one of the following option 👇 \n *A*. Covid-19 statistics *Worldwide*. \n *B*. Covid-19 Statistics in *countries*. \n *C*. Covid-19 News *Worldwide_*. \n *D*. How does it *Spread*? \n *E*. *Preventive measures* to be taken.\n\n*F*. *Report if you Suspect you have covid-19 virus🚑*\n\n*Please be adviced this is a test run.*")
                return(str(msg))
            else:
                data=get_data(msg_text,num)
                msg=MessagingResponse()
                resp=msg.message(data)
                return(str(msg))
        elif(status=="report"):
            collection.update_one({"NUMBER":num},{"$set":{"status":"location"}})
            msg=MessagingResponse()
            global fullname
            fullname=str(msg_text)
            
            resp=msg.message("*Please share your location*\n\nTo share your location click on 📎 then select location")
            return(str(msg))
           
        elif(status=="location"):
            msg=MessagingResponse()
            print(fullname)
            collections.insert_one({"NUMBER":num,"fullname":fullname,"latitude":lat,"longitude":lng})
            collection.update_one({"NUMBER":num},{"$set":{"status":"first"}})
            resp=msg.message("Your report has been received medical help will be provided as sson as possible\n\n")
            return (str(msg))
#endregion
