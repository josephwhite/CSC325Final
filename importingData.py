# Authors: Kevin Sangurima, Joseph White
# This code imports the data from an excel file to an online DB
# This code requires xlrd in order to read xlsx files 

import pymysql
import xlrd

def make_connection():
    return pymysql.connect(host='students.ce9mfwolh3f3.us-east-1.rds.amazonaws.com', user='admin', passwd='TempPassword123',
        port=3306, autocommit=True)

cnx = make_connection()
cur=cnx.cursor()


# Drops database if exists, if not then creates one
cur.execute('DROP DATABASE IF EXISTS GameAudioDB');
cur.execute('CREATE DATABASE GameAudioDB');
cur.execute('USE GameAudioDB');
# Drops all tables from the DB
cur.execute('DROP TABLE IF EXISTS Artists');
cur.execute('DROP TABLE IF EXISTS Albums');
cur.execute('DROP TABLE IF EXISTS Involvements');
cur.execute('DROP TABLE IF EXISTS Organizations');
# Creates the artists table
cur.execute('''CREATE TABLE Artists (
    id     INT NOT NULL PRIMARY KEY,
    name   NVARCHAR(100),
    gender nvarchar(10),
    dob DATE,
    type nvarchar(20)
)''');
# Creates the albums table
cur.execute('''CREATE TABLE Albums (
    id     INT NOT NULL PRIMARY KEY,
    name nvarchar(100),
    catalognum nvarchar(30),
    released DATE,
    price DECIMAL(10,2),
    length TIME 
)''');
# Creates the organizations table
cur.execute('''CREATE TABLE Organizations (
    id int NOT NULL PRIMARY KEY,
    name nvarchar(100),
    region nvarchar(80),
    type nvarchar(80)
)''');
# Creates the involvements table
cur.execute('''CREATE TABLE Involvements (
    id int NOT NULL PRIMARY KEY,
    artistid int,
    orgid int,
    role nvarchar(40),
    albumid int
)''');
# Reads the .xlsx file from the folder
book = xlrd.open_workbook('vgm.xlsx')
# Sets the index to the first sheet of the file
sheet = book.sheet_by_index(0)
# Insert statement for first table
query = """INSERT INTO Albums (id, name, catalognum, released, price, length) VALUES (%s, %s, %s, %s, %s, %s)"""

# loop over each row
for r in range(1, sheet.nrows):
    # extract each cell
    id   = sheet.cell(r,0).value
    name   = sheet.cell(r,1).value
    catalognum   = sheet.cell(r,2).value
    released   = sheet.cell(r,3).value
    price   = sheet.cell(r,4).value
    length   = sheet.cell(r,5).value
    # extract cells into pair
    values = id, name, catalognum, released, price, length

    # write pair to db
    cur.execute(query, values)
    
# Sets the index to the second sheet in the xlsx file
sheet = book.sheet_by_index(1)
# Insert statement for the second table
query = """INSERT INTO Artists (id, name, gender, dob, type) VALUES (%s, %s, %s, %s, %s)"""

# loop over each row
for r in range(1, sheet.nrows):
    # extract each cell
    id   = sheet.cell(r,0).value
    name   = sheet.cell(r,1).value
    gender   = sheet.cell(r,2).value
    dob   = sheet.cell(r,3).value
    type   = sheet.cell(r,4).value
    # extract cells into pair
    values = id, name, gender, dob, type

    # write pair to db
    cur.execute(query, values)
    
# Sets the index to the third sheet in the xlsx file
sheet = book.sheet_by_index(2)
# Insert statement for the third table
query = """INSERT INTO Organizations (id, name, region, type) VALUES (%s, %s, %s, %s)"""

# loop over each row
for r in range(1, sheet.nrows):
    # extract each cell
    id   = sheet.cell(r,0).value
    name   = sheet.cell(r,1).value
    region   = sheet.cell(r,2).value
    type   = sheet.cell(r,3).value
    # extract cells into pair
    values = id, name, region, type

    # write pair to db
    cur.execute(query, values)
    
# Sets the index to the fourth sheet in the xlsx file
sheet = book.sheet_by_index(3)
# Insert statement for the fourth table
query = """INSERT INTO Involvements (id, artistid, orgid, role, albumid) VALUES (%s, %s, %s, %s, %s)"""

# loop over each row
for r in range(1, sheet.nrows):
    # extract each cell
    id   = sheet.cell(r,0).value
    artistid   = sheet.cell(r,1).value
    orgid   = sheet.cell(r,2).value
    role   = sheet.cell(r,3).value
    albumid   = sheet.cell(r,4).value
    # extract cells into pair
    values = id, artistid, orgid, role, albumid

    # write pair to db
    cur.execute(query, values)

#Update a few broken data points on the excel file
cur.execute('''UPDATE Organizations 
    SET region = 'United States of America'
    WHERE region = 'United States of America.'
''')
cur.execute('''UPDATE Artists
    SET gender = 'N/A'
    WHERE gender = ''
''')
cur.execute('''UPDATE Organizations 
    SET region = 'Unknown'
    WHERE region = ''
''')
# close everything
cur.close()
cnx.commit()
cnx.close()

