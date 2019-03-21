import uuid

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.error as StoreErrors

class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id = None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store name {}>".format(self.name)

    def json(self):
        # return json represetation of the object
        return {
            'name': self.name,
            'url_prefix': self.url_prefix,
            '_id': self._id,
            'tag_name': self.tag_name,
            'query': self.query
        }


    def save_to_mongo(self):
        # pass the blog to mongoDb
        # instead insert data - we may need to update existing one = check by ID and decide if to insert or update
        #Database.insert(StoreConstants.COLLECTION, self.json())
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_id(cls, _id):
        store_data = Database.find_one(StoreConstants.COLLECTION, {'_id': _id})
        if store_data == None:
            return None
        else:
            return cls(**store_data)



    @classmethod
    def get_by_name(cls, name):
        store_data = Database.find_one(StoreConstants.COLLECTION, {'name': name})
        if store_data == None:
            return None
        else:
            return cls(**store_data)

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """
        return the store by URL prefix
        :param url_prefix:
        :return:
        """
        #we will use the url prefix a regualr expression search in MongoDB --> it should start with it
        store_data = Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": "^{}".format(url_prefix)}})
        #if store_data == None:
        #    return None
        #else:
        return cls(**store_data)


    @classmethod
    def find_by_url(cls, url):
        """
        return a store from full url of an item
        :param cls:
        :param url: the item URL
        :return: raise a store of StoreNotFoundExcetpion if not store match the URL
        """
        for i in range(1, len(url)+1):
            # start from the beginning of the url and try to find a complete match for the store url
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                # return None --> pass
                # instead we will return new exception
                raise StoreErrors.StoreNotFoundError("No Store was found for given  URL Prefix")

    @classmethod
    def get_stores(cls):
        return [cls(**store) for store in Database.find(StoreConstants.COLLECTION, {})]


    def remove_from_mongo(self):
        # remove the alert from mongoDb
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})