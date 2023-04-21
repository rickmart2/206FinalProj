import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/proj.db')
    cur = conn.cursor()

    path = os.path.dirname(os.path.abspath(__file__))
    cur.execute("SELECT WeatherData.temp, WeatherData.precip, WeatherData.windspeed, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date")
    data = cur.fetchall()
    
    with open (path+'/'+'calc.txt', 'w') as f:
        f.write('Temperature, Total Score, Stadium, Run Scored per Degree')
        f.write('\n')
        for item in data:
            if item[5] == 1:
                stadium = "Guarenteed Rate Field"
            else:
                stadium = "Wrigley Field"
            total = item[3] + item[4]
            temp = item[0]
            tot_p_temp = total/temp
            f.write(str(temp)+","+str(total)+","+str(stadium)+","+str(tot_p_temp))
            f.write("\n")
if __name__ == "__main__":
    main()