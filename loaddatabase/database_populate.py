#!/usr/bin/env python3
import sys
import pymysql
import csv
import os

# DATABASE_HOST isn't configured exit out
# if 'DATABASE_HOST' not in os.environ or os.environ['DATABASE_HOST'] == '':
#     print("No database configured exiting")
#     sys.exit(0)


population_sql = """
create table population (
LocID int(4),
Location nvarchar(200),
VarID int(4),
Variant nvarchar(50),
Time int(4),
MidPeriod float,
PopMale float,
PopFemale float,
PopTotal float,
PopDensity float
);
"""


with open('WPP2019_TotalPopulationBySex.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    population = list(reader)


# rds settings
#db_name = 'population'
rds_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
password = os.environ['DATABASE_PASSWORD']
db_name = os.environ['DATABASE_DB_NAME']
port = 3306

server_address = (rds_host, port)
conn = pymysql.connect(rds_host, user=db_user, passwd=password, db=db_name, connect_timeout=5, charset='utf8mb4')
cursor = conn.cursor()

cursor.execute("SHOW TABLES LIKE 'population'")
result = cursor.fetchone()
if not result:
    print("Creating population table")
    conn.cursor().execute(population_sql)
    conn.commit()

    print("Populating population table")
    for item in population:
        if (item['Variant'] == 'Medium' and int(item['Time']) <= 2019 and int(item['Time']) >= 1990):
            sql = """INSERT INTO `population` (LocID,Location,VarID,Variant,Time,MidPeriod,PopMale,PopFemale,PopTotal,PopDensity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (item["LocID"], item["Location"], item["VarID"], item['Variant'], item['Time'],
                                      item["MidPeriod"], item["PopMale"], item["PopFemale"], item['PopTotal'], item['PopDensity']))
                    conn.commit()
            except:
                print(("Unexpected error! ", sys.exc_info()))
                sys.exit("Error!")

conn.close()
