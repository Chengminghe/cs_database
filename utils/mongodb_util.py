from pymongo import MongoClient
import pandas as pd

class MongoQuery():
    def __init__(self,uri,database,collection):
        self.uri=uri
        self.database=database
        self.collection=collection
        self.client = MongoClient(uri)
    def query_topic_trend(self,input):
        collection = self.client[self.database][self.collection]
        pipeline = [
            {
                "$match": {
                    "keywords.name": "{}".format(input)
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": "$year"
                    },
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "_id.year": 1
                }
            }
        ]
        result = list(collection.aggregate(pipeline))
        df = pd.DataFrame(result)
        df['year'] = df._id.apply(lambda x:int(x['year']))
        df=df.drop('_id', axis=1)
        return df






