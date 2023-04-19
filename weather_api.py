import sqlite3
import requests
import json
import os


def collect_weather_data():
    
    chris_personal_key = 'P7VBY6VJVQZNFLJ8Y3D77HC6J'
    chris_cdogace_key = 'NKL9WMZAUEP446Q2TAL3GX7Z5'
    chris_umich_key = 'HZMD7PY4EZMQUUSWAUL5RJX4J'
    ricky_key = 'N2SH75WGJ6F9FS7VXMN4JLRMT'
    

    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/chicago/2022-04-07/2022-10-02?unitGroup=us&include=days&key={}&contentType=json"
    url = base_url.format(chris_umich_key)
    data = requests.get(url)
    data_dict = json.loads(data.text)
    # print(data_dict)

    cleaned_data_lst = []
    uniq_id = 1
    for day in data_dict["days"]:
        dashless_date = day["datetime"].replace("-", '')

        desired_data = {}
        desired_data["uniq_id"] = uniq_id
        desired_data["datetime"] = int(dashless_date)
        desired_data["temp"] = float(day["temp"])
        desired_data["feelslike"] = float(day["feelslike"])
        desired_data["precip"] = float(day["precip"])
        desired_data["windspeed"] = float(day["windspeed"])
        desired_data["visibility"] = float(day["visibility"])

        cleaned_data_lst.append(desired_data)
        uniq_id += 1
    
    #print(cleaned_data_lst)

    return cleaned_data_lst



def construct_data_base(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_weather_table(weather_info_lst, cur, conn, index_start):
    x = index_start    
    for dict_ in weather_info_lst[index_start: index_start+25]:
        uniq = dict_['uniq_id']

        date = dict_['datetime']

        temp = dict_['temp']

        feelslike = dict_['feelslike']

        precip = dict_['precip']

        windspeed = dict_['windspeed']

        visibility = dict_['visibility']

        cur.execute("INSERT OR IGNORE INTO WeatherData (uniq, date, temp, feelslike, precip, windspeed, visibility) VALUES (?, ?, ?, ?, ?, ?, ?)", (x, date, temp, feelslike, precip, windspeed, visibility))
        conn.commit()
        x += 1



def main():
    cur, conn = construct_data_base('proj.db')
    
    cur.execute("CREATE TABLE IF NOT EXISTS WeatherData (uniq INTEGER PRIMARY KEY, date INTEGER, temp REAL, feelslike REAL, precip REAL, windspeed REAL, visibility REAL)")
    cur.execute("SELECT max (uniq) from WeatherData")

    index_start = cur.fetchone()[0]
    print(index_start)
    if index_start == None:
        index_start = 0
    print(index_start)

    create_weather_table(collect_weather_data(), cur, conn, index_start)



if __name__ == '__main__':
    main()
