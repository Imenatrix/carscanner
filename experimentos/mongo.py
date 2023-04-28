from pymongo import MongoClient
import urllib.parse
import pandas as pd
import json

password = urllib.parse.quote_plus('imablu3b@nana')
url = 'mongodb+srv://imena:' + password + '@cluster0.3qmkpf1.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url)

data = pd.read_csv('sample.csv', index_col=0)
data = json.loads(data.to_json(orient='records'))

db = client['carscanner']
db['anuncios'].insert_many(data)
