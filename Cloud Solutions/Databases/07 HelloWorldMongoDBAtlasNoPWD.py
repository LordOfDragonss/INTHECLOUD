# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
import pymongo
from pymongo import MongoClient
import pandas as pd
import ssl

uri='mongodb+srv://mongoUser:*** pwd****@cluster0.hkfyo.mongodb.net/zipcode?retryWrites=true&w=majority'

client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)


client.list_database_names()

db=client.zipcode

df=pd.read_csv("population.csv")

db.population.insert_many(df.to_dict('records'))

