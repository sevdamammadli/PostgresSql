# -*- coding: utf-8 -*-
"""
Created on Tue May 31 21:26:05 2022

@author: sevdamammadli
"""

from sqlalchemy import create_engine
import pandas as pd

#connect to Postgresql db
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()#check connection

query = """
SELECT 1 
AS NUMBER
"""

pd.read_sql(query,con=engine)

#check for schemas (dont have any schema yet)
query = """
SELECT * 
FROM pg_catalog.pg_tables
WHERE schemaname!='pg_catalog' and
schemaname!='information_schema'
"""
pd.read_sql(query,con=engine)

url = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet"
dataset = pd.read_parquet(url)


dataset['tpep_pickup_datetime'] = pd.to_datetime(dataset['tpep_pickup_datetime'])
dataset['tpep_dropoff_datetime'] = pd.to_datetime(dataset['tpep_dropoff_datetime'])

#convert dataframe to db schema
print(pd.io.sql.get_schema(dataset,name="yellow_taxi_data",con=engine))

#import only data definition
dataset.head(0).to_sql(name='yellow_taxi_data',con=engine,if_exists='replace')

#append data 
dataset.to_sql(name='yellow_taxi_data',con=engine,if_exists='append',chunksize=100000)

#to see if we created the table in postgres
query = """
SELECT * 
FROM pg_catalog.pg_tables
WHERE schemaname!='pg_catalog' and
schemaname!='information_schema'
"""
pd.read_sql(query,con=engine)


#check number of rows
sql="""select count(*) from 
yellow_taxi_data"""

pd.read_sql(sql,con=engine)


