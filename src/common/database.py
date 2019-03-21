import os

import pymongo


class Database(object):
    URI = os.environ.get("MONGOLAB_URI")
     #                    ""mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        #gain access to the database and set the reference to static member
        Database.DATABASE = client['test']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)



    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        #upsert = 1 ==> if you can't find the data to update by query in DB insert the data
        Database.DATABASE[collection].update(query, data, upsert = True)

    @staticmethod
    def remove(collection, query):
        # upsert = 1 ==> if you can't find the data to update by query in DB insert the data
        Database.DATABASE[collection].remove(query, query)


