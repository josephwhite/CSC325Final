# Authors: Kevin Sangurima, Joseph White
# This code connects to the gameAudio Database and returns 5 queries which then are displayed
# on a 3x2 dashboard using matplotlib and pandas libraries.

import pymysql
import matplotlib.pyplot as plt
import pandas as pd 

mySQLCon = pymysql.connect(host='students.ce9mfwolh3f3.us-east-1.rds.amazonaws.com', user='admin', passwd='TempPassword123',
        port=3306, autocommit=True)
cur = mySQLCon.cursor();
# Query that tells the conection to use a specific DB
cur.execute("USE GameAudioDB")

# Query 1
df = pd.read_sql("SELECT DISTINCT role, Count(*) as Credits FROM Involvements WHERE role != 'owner' OR role != 'staff' GROUP BY role ORDER BY Credits;", mySQLCon)
# Creates a figure of size 17 x 9.5 (This will be used for the dashboard)
plt.figure(figsize=(17, 9.5)) 
# Plot 1
plt.subplot(321) 
plt.bar(df['role'], df['Credits']) 
plt.xlabel("Role") 
plt.ylabel("Credits") 
plt.title('Credits per Role', fontsize=16) 

# Query 2
df = pd.read_sql("SELECT DISTINCT o.Region, COUNT(i.albumid) AS Alb_Count FROM Organizations o INNER JOIN Involvements i on o.id = i.orgid GROUP BY o.region ORDER BY o.region;", mySQLCon)

# Plot 2
plt.subplot(322) 
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = df['Region']
sizes = df['Alb_Count']
explode = (0, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')  
plt.title('Region Where Album Was Released', fontsize=16)

# Query 3
df = pd.read_sql("SELECT DISTINCT YEAR(released) AS Year_Released, AVG(price) AS Avg_Price FROM Albums GROUP BY YEAR(released) ORDER BY YEAR(released);", mySQLCon)

# Plot 5
plt.subplot(325) 
plt.plot(df['Year_Released'], df['Avg_Price'])
plt.xlabel("Year Released")
plt.ylabel("Average Price")
plt.title('Average Price x Year Released', fontsize=16)

# Query 4
df = pd.read_sql("SELECT Count(*) AS Num, gender FROM Artists Group by gender;", mySQLCon)

# Plot 3
plt.subplot(323) 
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = df['gender']
sizes = df['Num']
explode = (0, 0, 0)  
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')  
plt.title('Artist Gender', fontsize=16)

# Query 5
df = pd.read_sql("SELECT name, price FROM Albums Order by price desc limit 5;", mySQLCon)

# Plot 4
plt.subplot(324) 
plt.bar(df['name'], df['price']) 
plt.xticks(rotation=40)
plt.xlabel("Rank") 
plt.ylabel("Price") 
plt.title('Top 5 Highest Prices of Game Albums', fontsize=16)


# Adds spacing in between all of the plots
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=.45)
# Adds a title to the dashboard
plt.suptitle("Game Audio Database", fontsize=20)
# Displays the dashboard
plt.show() 

