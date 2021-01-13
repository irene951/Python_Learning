import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib.request as req
import bs4

#利用BS4抓取並解讀網頁HTML-------------------------------------------------------------------------------------------

url="https://www.basketball-reference.com/teams/GSW/2016.html"
request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
root=bs4.BeautifulSoup(data,"html.parser")

#開始擷取特定部分
ranker=root.find('table',attrs={"id" : "per_game"}).find_all('th',attrs={'scope':"row"})#編號
number=[]
for i in ranker:
    number.append(int(i.string))
columnname=['player','MP','FGA','FTA','TOV']
data=pd.DataFrame(columns=columnname,index=number)
x=1
players=root.find('table',attrs={"id" : "per_game"}).find_all('td',attrs={"data-stat" : "player"})#球員名稱
for i in players:
    data.loc[x,['player']]=i.string
    x+=1
x=1
y=1
for i in ['mp_per_g','fga_per_g','fta_per_g','tov_per_g']:
    catchdata=root.find('table',attrs={"id" : "per_game"}).find_all('td',attrs={"data-stat" : i})
    for j in catchdata:
        data.loc[x,[columnname[y]]]=float(j.string)
        x+=1
    x=1
    y+=1

#全部寫成一個for迴圈，建立陣列for item in ['MP','FGA','FTA','TOV']
USGPdataframe=pd.DataFrame(columns=["player","USPG"],index=number)
USGPdataframe["player"]=data["player"]
for i in range(1,17):
    USGP=(data["FGA"][i]+0.44*data["FTA"][i]+data["TOV"][i])*(data["MP"].sum()/5)/data["MP"][i]/(data['FGA'].sum()+0.44*data['FTA'].sum()+data['TOV'].sum())*100
    USGPdataframe["USPG"][i]=USGP

#整理資料，繪圖-----------------------------------------------------------------------------------------------------------------------------------------------------------------

theset = frozenset(USGPdataframe["USPG"].head()) #取前五項並固定
theset = sorted(theset,reverse = True) #大到小排列

usage = []

i = 0
while(i<5):
    usage.append(round(theset[i],4))
    i+=1

#繪圖

fig = plt.figure()

col_count = 5
bar_width = 0.4
index = (1, 1, 1)

plt.ylabel("Players")          # 設定y軸標題 
plt.xlabel("Usage%")            # 設定x軸標題
plt.title("Bar chart of Top Usage% Player in GSW(15-16)", {'fontsize' : 17})
plt.xticks(fontsize = 7)


left = np.array([1, 2, 3, 4, 5])
Players = ["Stephen Curry", "Marreese Speights", "Klay Thompson", "James Michael McAdoo", "Ian CLark"]
rgb = ["midnightblue", "darkmagenta", "forestgreen", "goldenrod", "indianred"]

plt.bar(left, usage, width = bar_width, color= rgb, tick_label=Players)
plt.show()