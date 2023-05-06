import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
from ast import literal_eval

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
df.drop("id_artists", inplace=True, axis=1)


df['release_date'] = pd.to_datetime(df['release_date'],format='ISO8601')
df['year'] = df['release_date'].dt.year
df.drop("release_date", inplace=True, axis=1)
df = df[df.explicit == 1]
df.artists = df.artists.apply(literal_eval)
df.info()

# insert data into collection
data = df.to_dict('records')
collection.insert_many(data)

# group documents by year and calculate average acousticness and energy
pipeline = [
    {"$group": {
        "_id": {"$arrayElemAt": ["$artists", 0]},
        "popularity": {"$avg": "$popularity"}
    }},
    {"$sort": {"popularity": -1}},
    {"$limit": 10}
]
result = list(collection.aggregate(pipeline))

# plot the data
df = pd.DataFrame(result)
plt.figure(figsize=(16, 8))
plt.bar(df._id, df.popularity)
plt.xlabel("Top Artists")
plt.ylabel("Average Popularity")
plt.title("Top 10 Artists by Popularity of Explcicit Songs")
plt.legend()
plt.show()
