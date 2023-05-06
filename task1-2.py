import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# group documents by popularity and calculate average acousticness and energy
pipeline = [
    {"$group": {
        "_id": "$popularity",
        "avg_loudness": {"$avg": "$loudness"},
    }}
]
result = list(collection.aggregate(pipeline))

df = pd.DataFrame(result)

sns.set(style="whitegrid")
sns.lineplot(data=df, x="_id", y="avg_loudness", label="Average Acousticness")
plt.xlabel("Popularity")
plt.ylabel("Attribute Value")
plt.title("Average Loudness by Popularity")
plt.legend()
plt.show()
