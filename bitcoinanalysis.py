import pandas as pd
import csv
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
now = datetime.now()


anaylze_choice = """
=============================
(1). See All
(2). See First & Last
(3). See Custom Date/Time
=============================
"""

def scrape():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    url = requests.get("https://www.google.com/search?q=bitcoin+idr" , headers = headers)
    soup = BeautifulSoup(url.text , 'lxml')
    price_idr = soup.find("span" , class_ = "pclqee").text  
    return price_idr  

def get_time():
    time1 = now.strftime("%H:%M:%S")
    return time1

def get_date():
    date1 = now.strftime("%d/%m/%y")
    return date1

def get_change(price_now):
    panda_dataframe = pd.read_csv("bitcoinanalysis.csv")
    price_old = panda_dataframe["BTC price"].tail(1).to_string(index = False)

    price_old_formatted = str(price_old).replace("." , "")
    price_old_formatted = price_old_formatted.replace("," , ".")

    price_now_formatted = str(price_now).replace("." , "")
    price_now_formatted = price_now_formatted.replace("," , ".")

    try:
        if float(price_now_formatted) > float(price_old_formatted):
            difference = float(price_now_formatted) - float(price_old_formatted)
            Increase = difference / float(price_old_formatted) * 100
            return "+" + str(Increase) + "%"
        
        elif float(price_now_formatted) < float(price_old_formatted):
            difference = float(price_old_formatted) - float(price_now_formatted)
            decrease = difference / float(price_old_formatted) * 100
            return "-" + str(decrease) + "%"
        
        else:
            return "None"

    except ValueError:
        return "None"
   
def main():
    while True:
        find_price_or_anaylise = input("Find Price Or Analyze The Data (F/A) : ")
        if find_price_or_anaylise.lower() == "f" :
            howmanytimes = input("How Many Times? : ")
            if howmanytimes.isnumeric() == True and len(howmanytimes) > 0 :
                for x in range(int(howmanytimes)):
                    price_now = scrape()
                    timexd = get_time()
                    datexd = get_date()
                    change = get_change(price_now)
                    with open("bitcoinanalysis.csv" , 'a') as csv_file :
                        writer = csv.writer(csv_file)
                        writer.writerow([str(timexd),str(datexd),str(price_now),str(change)])
                    print("")
                    print("Finished Written")
                    print("Waiting....")
                    print("")
                    time.sleep(40)
                
            else:
                print("Invalid")
        
        elif find_price_or_anaylise.lower() == "a":
            print(anaylze_choice)
            df = pd.read_csv("bitcoinanalysis.csv")
            choice = input("Pick Your Number : ")
            if choice == "1" :
                print(df)
            
            elif choice == "2":
                print(f"First: {df.head(1)}")
                print("")
                print(f"Last: {df.tail(1)}")
            
            elif choice == "3":
                date_or_time = input("Date Or Time Or Date & Time (D,T,DT):")
                if date_or_time.lower() == "d":
                    date_input = input("Date ex.(01/01/2001) : ")
                    print(df.loc[df["date"] == date_input])
                
                elif date_or_time.lower() == "t":
                    time_input = input("Time ex.(00:00:00) : ")
                    print(df.loc[df["time"] == time_input])
                
                elif date_or_time.lower() == "dt":
                    date_input = input("Date ex.(01/01/2001) : ")
                    time_input = input("Time ex.(00:00:00) : ")
                    stage_1 = df.loc[df["date"] == date_input] 
                    print(stage_1.loc[df["time"] == time_input])
            
   

            

main()    