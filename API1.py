import sqlite3
import requests
import json
import os



def getMLBdata():
    data = requests.get("https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-04-07&endDate=2022-10-02")
    info_dict = json.loads(data.text)
    orig_list = []
    lst2 = []

    for item in info_dict['dates']:
        for thing in item["games"]:
            if thing["venue"]["name"] == 'Wrigley Field' or thing["venue"]["name"] == "Guaranteed Rate Field" and thing['status']['statusCode'] == 'F':
                orig_list.append(thing)
    for item in orig_list:
        temp_dict = {}
        try:
            
            temp_dict["date"] = item['officialDate'].replace("-", '')
            temp_dict['away_score'] = dict(item['teams']['away'])['score']
            temp_dict['home_score'] = item['teams']['home']['score']
            if item['venue']['name'] == "Wrigley Field":
                temp_dict['stadium'] = 0
            else:
                temp_dict['stadium'] = 1
        except:
            continue
        
        lst2.append(temp_dict)
    return lst2
getMLBdata()

def setUpDb(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+"/"+db_name)
    cur = conn.cursor()
    return cur, conn

def createMLBtab(cur, conn, lst, start):
    x = start
    for i in lst[start: start+25]:
        home = str(i["home_score"])
        away = str(i["away_score"])
        stadium = str(i["stadium"])
        date = str(i["date"])
        cur.execute("INSERT OR IGNORE INTO Mlb (id, home_score, away_score, stadium, date) VALUES (?,?,?,?,?)", (x, home, away, stadium, date))
        conn.commit()
        x += 1

def main():
    cur, conn = setUpDb('proj.db')
    cur.execute("CREATE TABLE IF NOT EXISTS Mlb (id NUMBER PRIMARY KEY, home_score NUMBER, away_score NUMBER, stadium NUMBER, date NUMBER)")
    cur.execute("SELECT max (id) from Mlb")
    

    start = cur.fetchone()[0]
    print(start)
    if start == None:
        start = 0
    print(start)
    createMLBtab(cur, conn, getMLBdata(), start)
   #print(getMLBdata())
if __name__ == "__main__":
    main()






