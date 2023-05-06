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

# group documents by year and calculate average acousticness and energy
pipeline = [
    {"$group": {
        "_id": "$year",
        "avg_acousticness": {"$avg": "$acousticness"},
        "avg_energy": {"$avg": "$energy"}
    }}
]
result = list(collection.aggregate(pipeline))

df = pd.DataFrame(result)

sns.set(style="whitegrid")
sns.lineplot(data=df, x="_id", y="avg_acousticness", label="Average Acousticness")
sns.lineplot(data=df, x="_id", y="avg_energy", label="Average Energy")
plt.xlabel("Year")
plt.ylabel("Attribute Value")
plt.title("Average Acousticness and Energy by Year")
plt.legend()
plt.show()
