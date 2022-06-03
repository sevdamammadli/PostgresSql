# PostgreSql


Running Postgres with Docker

Running on windows (use full path)

```
docker run it- \
   --name postgresql \
   -e POSTGRES_USER=myusername \
   -e POSTGRES_PASSWORD=mypassword \
   -e POSTGRES_DB="db” \
   -p 5432:5432
   -v /data:/var/lib/postgresql/data
   postgres:13

```
Create Connection to Postgres using Pandas

```
from sqlalchemy import create_engine
import pandas as p

#connect to Postgresql db
engine = create_engine('postgresql://root:root@localhost:5432/db')
engine.connect()
```
Read Data and convert text to datetime
```
url = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet"
dataset = pd.read_parquet(url)
dataset['tpep_pickup_datetime'] = pd.to_datetime(dataset['tpep_pickup_datetime'])
dataset['tpep_dropoff_datetime'] = pd.to_datetime(dataset['tpep_dropoff_datetime'])
```

convert dataframe to db schema
```
print(pd.io.sql.get_schema(dataset,name="yellow_taxi_data",con=engine))
```
import only data definition
```
dataset.head(0).to_sql(name='yellow_taxi_data',con=engine,if_exists='replace')
```

append data to table
```
dataset.to_sql(name='yellow_taxi_data',con=engine,if_exists='append',chunksize=100000)
```

Finally, check if we created the table in postgres
```
query = """
SELECT * 
FROM pg_catalog.pg_tables
WHERE schemaname!='pg_catalog' and
schemaname!='information_schema'
"""
pd.read_sql(query,con=engine)
```


