# Authors: Kevin Sangurima, Joseph White
# This code converts the data from JSON to an excel file

import json
import requests
import datetime
import numpy as np
import xlsxwriter as excel

def unique(list1):
    x = np.array(list1)
    distinct = np.unique(x)
    return distinct


albums = [27, 37, 72, 79, 282, 353, 373, 411, 443, 497, 522, 536, 718, 1034, 1222, 1541, 1554, 1156, 1640, 1649, 1678, 2411, 2877, 2898, 4000, 4247, 4393, 4463, 4772, 5225, 7431, 10424, 10599, 11048, 14243, 21668, 21864, 22763, 23311, 26577, 29979, 30020, 33289, 35660, 37624, 41306, 41746, 44071, 45088, 47017, 54247, 64624, 65654, 71214, 71570, 71954, 73671, 80807]
artists = []
organizations = []

# Creates a conversion rate for Japanese Yen to United States Dollars
url = "https://api.exchangerate-api.com/v4/latest/JPY"
moneylink = requests.get(url)
cashchain = moneylink.json()
jpy2usd_rate = cashchain["rates"]["USD"]

# Creates Excel file and sheets.
workbook = excel.Workbook('vgm.xlsx')
albumsheet = workbook.add_worksheet("Albums")
artistsheet = workbook.add_worksheet("Artists")
organizationsheet = workbook.add_worksheet("Organizations")
involvementsheet = workbook.add_worksheet("Involvements")

row = 0
col = 0
involveId = 0

for i in albums:
    link = "https://vgmdb.info/album/" + str(i) + "?format=json"
    give = requests.get(link)
    art = json.loads(give.text)
    totalTime = datetime.timedelta()
    # For every row in the Albums table, there will be columns for (1alb) a unique identifyer, (2alb) album name, (3alb) catalog number, (4alb) release date, ...
    albumsheet.write(row, col, i)
    albumsheet.write(row, col+1, art["name"])
    albumsheet.write(row, col+2, art["catalog"])
    albumsheet.write(row, col+3, art["release_date"])
    # ... (5alb) the price in USD (convert if nessesary), ...
    if art["release_price"]["currency"] == "JPY":
        usd = int(art["release_price"]["price"]) * jpy2usd_rate
        usd = round(usd, 2)
        albumsheet.write(row, col+4, usd)
    elif art["release_price"]["currency"] == "USD":
        usd = (art["release_price"]["price"])
        albumsheet.write(row, col+4, usd)
    # For every arranger in the album with an id, add (1inv) a unique identifyer, (2inv) the artist's id, (4inv) the name of the role, and (5inv) the album's id to the Involvements table.
    for arranger in art["arrangers"]:
        if ("link" in arranger):
            rat,splat = arranger["link"].split("/")
            artists.append(splat)
            involvementsheet.write(involveId, col, involveId)
            involvementsheet.write(involveId, col+1, splat)
            involvementsheet.write(involveId, col+3, "arranger")
            involvementsheet.write(involveId, col+4, i)
            involveId+=1
    # For every composer in the album with an id, add (1inv) a unique identifyer, (2inv) the artist's id, (4inv) the name of the role, and (5inv) the album's id to the Involvements table.
    for composer in art["composers"]:
        if ("link" in composer):
            #print("Composer: " + composer["names"]["en"])
            rat,splat = composer["link"].split("/")
            artists.append(splat)
            involvementsheet.write(involveId, col, involveId)
            involvementsheet.write(involveId, col+1, splat)
            involvementsheet.write(involveId, col+3, "composer")
            involvementsheet.write(involveId, col+4, i)
            involveId+=1
    # For every performer in the album with an id, add (1inv) a unique identifyer, (2inv) the artist's id, (4inv) the name of the role, and (5inv) the album's id to the Involvements table.
    for performer in art["performers"]:
        if ("link" in performer):
            #print("Performer: " + performer["names"]["en"])
            rat,splat = performer["link"].split("/")
            artists.append(splat)
            involvementsheet.write(involveId, col, involveId)
            involvementsheet.write(involveId, col+1, splat)
            involvementsheet.write(involveId, col+3, "performer")
            involvementsheet.write(involveId, col+4, i)
            involveId+=1
    # For every lyricist in the album with an id, add (1inv) a unique identifyer, (2inv) the artist's id, (4inv) the name of the role, and (5inv) the album's id to the Involvements table.
    for lyricist in art["lyricists"]:
        if ("link" in lyricist):
            #print("Lyricist: " + lyricist["names"]["en"])
            rat,splat = lyricist["link"].split("/")
            artists.append(splat)
            involvementsheet.write(involveId, col, involveId)
            involvementsheet.write(involveId, col+1, splat)
            involvementsheet.write(involveId, col+3, "lyricist")
            involvementsheet.write(involveId, col+4, i)
            involveId+=1
    # For every organization in the album with an id, add (1inv) a unique identifyer, (3inv) the organization's id, (4inv) the name of the role, and (5inv) the album's id to the Involvements table.
    for orgs in art["organizations"]:
        if ("link" in orgs):
            print(orgs["role"] + ": " + orgs["names"]["en"])
            rat,splat = orgs["link"].split("/")
            organizations.append(splat)
            involvementsheet.write(involveId, col, involveId)
            involvementsheet.write(involveId, col+2, splat)
            involvementsheet.write(involveId, col+3, orgs["role"])
            involvementsheet.write(involveId, col+4, i)
            involveId+=1
    # ... (6alb) and the total length of the album across all discs.
    for disc in art["discs"]:
        s = disc["disc_length"]
        min, sec = s.split(":")
        min_int = int(min)
        sec_int = int(sec)
        delt = datetime.timedelta(seconds=sec_int, minutes=min_int, hours=0)
        totalTime += delt
    albumsheet.write(row, col+5, str(totalTime))
    row+=1

# Create a unique array of organizations
row = 0
unique_org = unique(organizations)

# For every row in the Organizations table, there will be columns for (1org) a unique identifier, (2org) the organization name, (3org) the region, (4org) and the type of organization.
for k in unique_org:
    link = "https://vgmdb.info/org/" + str(k) + "?format=json"
    give = requests.get(link)
    art = json.loads(give.text)
    organizationsheet.write(row, col, k)
    organizationsheet.write(row, col+1, art["name"])
    organizationsheet.write(row, col+2, art["region"])
    organizationsheet.write(row, col+3, art["type"])
    for staff in art["staff"]:
        if ("link" in staff):
            rat,splat = staff["link"].split("/")
            artists.append(splat)
            involvementsheet.write(involveId, col, involveId)
            involvementsheet.write(involveId, col+1, splat)
            involvementsheet.write(involveId, col+2, k)
            if (staff["owner"]  == False):
                involvementsheet.write(involveId, col+3, "staff")
            else:
                involvementsheet.write(involveId, col+3, "owner")
            involveId+=1
    row+=1

# Create a unique array of artists
row = 0
unique_artist = unique(artists)

# For every row in the Artists table, there will be columns for (1art) a unique identifier, (2art) the artist's name, (3art) their gender, (4art) dob, (5art) type of artist.
for j in unique_artist:
    link = "https://vgmdb.info/artist/" + str(j) + "?format=json"
    give = requests.get(link)
    art = json.loads(give.text)
    artistsheet.write(row, col, j)
    artistsheet.write(row, col+1, art["name"])
    if ("sex" in art):
        artistsheet.write(row, col+2, art["sex"])
    if ("birthdate" in art and "0000" not in art["birthdate"]):
        artistsheet.write(row, col+3, art["birthdate"])
    if ("type" in art):
        artistsheet.write(row, col+4, art["type"])
    row+=1

workbook.close()
