import re
import uuid

import requests
from bs4 import BeautifulSoup

from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price = None, _id=None):
        self.name = name
        store = Store.find_by_url(url)
        self.url = url
        # store hold the name of the element that represent price
        self.tag_name = store.tag_name
        # store will hold the specific query with attributes that match the tag
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    #we may not have price during creation
    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        """
        loads an item's data using their store and return a JSON representation for it
        """
        # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$174.00</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        # remove white spaces
        str_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)") # represent decimal number
        # look for pattern in str price
        match = pattern.search(str_price)
        self.price = float(match.group())
        return self.price


    def json(self):
        # return json represetation of the object
        return {
            '_id': self._id,
            'name': self.name,
            'url': self.url,
            'price': self.price
        }


    def save_to_mongo(self):
        # pass the blog to mongoDb
        # instead insert data - we may need to update existing one = check by ID and decide if to insert or update
        # Database.insert(ItemConstants.COLLECTION, self.json())
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())


    @classmethod
    def get_by_name(cls, name):
        item_data = Database.find_one(ItemConstants.COLLECTION, {'name': name})
        if item_data == None:
            return None
        else:
            return cls(**item_data)




    @classmethod
    def get_by_id(cls, _id):
        item_data = Database.find_one(ItemConstants.COLLECTION, {'_id': _id})
        if item_data == None:
            return None
        else:
            return cls(**item_data)
