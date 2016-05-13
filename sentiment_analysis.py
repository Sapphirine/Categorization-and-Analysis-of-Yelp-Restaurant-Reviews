from pymongo import MongoClient

from settings import Settings
from alchemyapi import AlchemyAPI

reviews_collection = MongoClient(Settings.MONGO_CONNECTION_STRING)[Settings.REVIEWS_DATABASE][
    Settings.TEST_COLLECTION]
reviews_cursor = reviews_collection.find({},{'text':1})
alchemyapi = AlchemyAPI()

for reviews in reviews_cursor:
        response = alchemyapi.sentiment("text", reviews)
        print reviews
        sentiment=response["docSentiment"]["type"]
        reviews_collection.update({'sentiment': ""},{'$set':{"sentiment":sentiment
                              }})
