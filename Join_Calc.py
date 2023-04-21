import sqlite3
import os
import numpy as np
import matplotlib.pyplot as plt


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
                stadium = "Guaranteed Rate Field"
            else:
                stadium = "Wrigley Field"
            total = item[3] + item[4]
            temp = item[0]
            tot_p_temp = total/temp
            f.write(str(temp)+","+str(total)+","+str(stadium)+","+str(tot_p_temp))
            f.write("\n")

# Visualization 1

    fig = plt.figure(figsize=(15,8))
    fig.subplots_adjust(hspace=0.5)
    ax1 = fig.add_subplot(223)
    cur.execute('SELECT date,home_score FROM Mlb where stadium = ?', (0, ))
    info = cur.fetchall()
    cur.execute("SELECT WeatherData.temp, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (0, ))
    vis1data = cur.fetchall()
    print(len(vis1data))
    lstx = []
    for item in vis1data:
        total = item[1] + item[2]
        temp = item[0]
        tot_p_temp = total/temp
        lstx.append(tot_p_temp)

    days_into_season = []
    

    i = 1
    for date in info:
        days_into_season.append(i)

        i += 1

    x = days_into_season
    y = lstx
    ax1.plot(x, y, label='Wrigley Field', color='blue')

    #________________________________________________________________________________________________________

    cur.execute('SELECT date,home_score FROM Mlb where stadium = ?', (1, ))
    info2 = cur.fetchall()

    cur.execute("SELECT WeatherData.temp, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (1, ))
    vis1data2 = cur.fetchall()
    print(len(vis1data2))
    lstx2 = []
    for item in vis1data2:
        total2 = item[1] + item[2]
        temp2 = item[0]
        tot_p_temp2 = total2/temp2
        lstx2.append(tot_p_temp2)

    days_into_season2 = []

    

    i2 = 1
    for date in info2:
        days_into_season2.append(i2)

        i2 += 1

    x2 = days_into_season2
    y2 = lstx2
    ax1.plot(x2, y2, label='Guaranteed Rate Field', linestyle = ":", color='red')

    ax1.set(xlabel="Games Into Season", ylabel="Runs Scored per Degree", title="Runs Scored per Degree Over Course of Season")
    ax1.legend()


# Visualization 2


    ax2 = fig.add_subplot(222)
    
    cur.execute("SELECT WeatherData.precip, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (0, ))
    vis2data = cur.fetchall()

    lst_scatter_1_total = []
    lst_scatter_1_precip = []
    for item in vis2data:
        total = item[1] + item[2]
        precip = item[0]
        
        lst_scatter_1_total.append(total)
        lst_scatter_1_precip.append(precip)


    x3 = lst_scatter_1_precip
    y3 = lst_scatter_1_total
    lst_scatter_1_precip
    ax2.scatter(x3, y3, label='Wrigley Field', color='blue')

    a3, b3 = np.polyfit(x3, y3, 1)
    plt.plot(x3, a3*np.array(x3)+b3)

    #________________________________________________________________________________________________________

    cur.execute("SELECT WeatherData.precip, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (1, ))
    vis3data = cur.fetchall()

    lst_scatter_2_total = []
    lst_scatter_2_precip = []
    for item in vis3data:
        total = item[1] + item[2]
        precip = item[0]
        
        lst_scatter_2_total.append(total)
        lst_scatter_2_precip.append(precip)


    x4 = lst_scatter_2_precip
    y4 = lst_scatter_2_total
   
    ax2.scatter(x4, y4, label='Guaranteed Rate Field', color='red')

    ax2.set(xlabel="Precipitation", ylabel="Total Runs", title="Relationship Between Precipitation and Total Runs Scored")
    ax2.legend()

    a4, b4 = np.polyfit(x4, y4, 1)
    plt.plot(x4, a4*np.array(x4)+b4)


# Visualization 3


    ax3 = fig.add_subplot(221)
    
    cur.execute("SELECT WeatherData.windspeed, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (0, ))
    vis3data = cur.fetchall()

    lst_scatter_3_total = []
    lst_scatter_1_windspeed = []
    for item in vis3data:
        total = item[1] + item[2]
        windspeed = item[0]
        
        lst_scatter_3_total.append(total)
        lst_scatter_1_windspeed.append(windspeed)


    x5 = lst_scatter_1_windspeed
    y5 = lst_scatter_3_total
    
    ax3.scatter(x5, y5, label='Wrigley Field', color='blue')

    a5, b5 = np.polyfit(x5, y5, 1)
    plt.plot(x5, a5*np.array(x5)+b5)

    #________________________________________________________________________________________________________

    cur.execute("SELECT WeatherData.windspeed, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (1, ))
    vis4data = cur.fetchall()

    lst_scatter_4_total = []
    lst_scatter_2_windspeed = []
    for item in vis4data:
        total = item[1] + item[2]
        windspeed = item[0]
        
        lst_scatter_4_total.append(total)
        lst_scatter_2_windspeed.append(windspeed)


    x6 = lst_scatter_2_windspeed
    y6 = lst_scatter_4_total
    
    ax3.scatter(x6, y6, label='Guaranteed Rate Field', color='red')

    ax3.set(xlabel="Windspeed", ylabel="Total Runs", title="Relationship Between Windspeed and Total Runs Scored")
    ax3.legend()

    a6, b6 = np.polyfit(x6, y6, 1)
    plt.plot(x6, a6*np.array(x6)+b6)


# Visualization 4


    ax4 = fig.add_subplot(224)
    
    cur.execute("SELECT WeatherData.feelslike, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (0, ))
    vis4data = cur.fetchall()

    lst_scatter_5_total = []
    lst_scatter_1_feelslike = []
    for item in vis4data:
        total = item[1] + item[2]
        feelslike = item[0]
        
        lst_scatter_5_total.append(total)
        lst_scatter_1_feelslike.append(feelslike)


    x7 = lst_scatter_1_feelslike
    y7 = lst_scatter_5_total
    
    ax4.scatter(x7, y7, label='Wrigley Field', color='blue')

    a7, b7 = np.polyfit(x7, y7, 1)
    plt.plot(x7, a7*np.array(x7)+b7)

    

    #________________________________________________________________________________________________________

    cur.execute("SELECT WeatherData.feelslike, Mlb.home_score, Mlb.away_score, Mlb.stadium from Mlb LEFT JOIN WeatherData ON Mlb.date = WeatherData.date where stadium = ?", (1, ))
    vis5data = cur.fetchall()

    lst_scatter_6_total = []
    lst_scatter_2_feelslike = []
    for item in vis5data:
        total = item[1] + item[2]
        feelslike = item[0]
        
        lst_scatter_6_total.append(total)
        lst_scatter_2_feelslike.append(feelslike)


    x8 = lst_scatter_2_feelslike
    y8 = lst_scatter_6_total
    
    ax4.scatter(x8, y8, label='Guaranteed Rate Field', color='red')

    ax4.set(xlabel="Wind Chill", ylabel="Total Runs", title="Relationship Between Wind Chill and Total Runs Scored")
    ax4.legend()

    a8, b8 = np.polyfit(x8, y8, 1)
    plt.plot(x8, a8*np.array(x8)+b8)

    plt.show()
    


if __name__ == "__main__":
    main()