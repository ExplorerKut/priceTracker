from bs4 import BeautifulSoup
import os
import shutil
import plotly.express as px
import plotly.graph_objects as go
from os.path import exists,isdir
import requests
import re
import pandas as pd
from datetime import datetime
url_desired_price=dict()
product_name_list=list()
try:
    #This block goes through your tracking list and creates a dictionary with the url as key and desired price as it's value
    try:
        with open("trackingList.txt","r") as trackingList:
            for list in trackingList:
                url,price=list.split(",")
                url_desired_price.update({str(url):int(price)})
    except Exception as e:
        raise e
    try:
        header = {
            "referer":"www.amazon.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"
        }
        # print(url_desired_price)
        for key,value in url_desired_price.items():
            # print(key)
            # print(key)
            page=requests.get(key,headers=header)
            # print(page)
            # print(datetime.now())
            request_time=datetime.timestamp(datetime.now())
            soup=BeautifulSoup(page.content,"lxml")
            # print(soup.prettify())
            # with open("priceTracker.html","w") as ft:
            #     ft.write(soup.prettify())
            product_name=soup.find(id="productTitle").text.lstrip().rstrip().replace(" ","_")[0:15]
            product_price=soup.find("span",class_="a-price-whole").text
            product_price=re.sub('[^A-Za-z0-9]+', '', product_price)
            product_name_list.append(product_name+".csv")
            file_exists=isdir("updates")        
            if not file_exists:
                os.mkdir("updates")


            file_exists=exists("updates/"+product_name+".csv")


            if not file_exists:

                with open("updates/"+product_name+".csv","w") as file_new:
                    file_new.write("dateUpdated"+","+"price")   
 
 
            with open("updates/"+product_name+".csv","a") as file_existing:
                file_existing.write("\n"+str(request_time)+","+str(product_price))
        
        check_csv_file=[file_name for file_name in os.listdir('updates')]
        for file_name in check_csv_file:
            if file_name not in product_name_list:
                os.remove("updates/"+file_name)
        file_exists=isdir("graphs")
        if file_exists:
            shutil.rmtree("graphs")
        os.mkdir("graphs")
        for csv in os.listdir('updates'):
            csv_file=pd.read_csv('updates/'+csv);
            csv_file['dateUpdated']=pd.to_datetime(csv_file['dateUpdated'],unit='s')
            # print(csv_file)
            # csv_file.plot(x="dateUpdated",y="price",kind="line")
            # pp.plot(csv_file["dateUpdated"],csv_file["price"])
            # pp.savefig(csv+".png")
            
            fig=px.line(csv_file,x="dateUpdated",y="price")
            # fig=go.Figure([go.Scatter(x=csv_file['dateUpdated'],y=csv_file['price'])])
            
            fig.write_image("graphs/"+csv+".jpeg")

    except Exception as e:
        raise e
except Exception as e:
    raise e

