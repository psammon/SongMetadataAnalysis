import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import datetime

# connecting to our mongodb collection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["spotify-data"]

# start with fresh collection
result = collection.delete_many({})

# read in data.csv with pandas
df = pd.read_csv('cs471-nosql/tracks.csv')
# df.info()

# clean up data
df.drop("id", inplace=True, axis=1)
df.drop("name", inplace=True, axis=1)
df.drop("artists", inplace=True, axis=1)
df.drop("id_artists", inplace=True, axis=1)

df['release_date'] = pd.to_datetime(df['release_date'],format='ISO8601')
df['year'] = df['release_date'].dt.year
df.drop("release_date", inplace=True, axis=1)

df.info()

# insert data into collection
data = df.to_dict('records')
collection.insert_many(data)

# create and show correlation heatmap using pandas and seaborn
plt.figure(figsize=(16, 8))
corr = df.corr()
sb.heatmap(corr,annot=True, cmap="YlGnBu")
plt.show()
