import datetime
import uuid

import requests

import src.models.alerts.constants as AlertConstants
import src.models.alerts.errors as AlertErrors
from src.common.database import Database

from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, is_active=True, last_checked=None, _id=None):
        self.user_email = user_email

        self.price_limit = price_limit
        self.item_id = item_id
        self.item = Item.get_by_id(item_id)
        self.is_active = is_active
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    # teh representaion of object as string in case we print it
    def __repr__(self):
        return "<Alert for {} on item {} with price {}".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
		AlertConstants.URL,
		auth=("api", AlertConstants.API_KEY),
		data={"from": AlertConstants.FROM,
			"to": self.user_email,
			"subject": "Price limit reached for {}".format(self.item.name),
			"text": "we found a deal {}. To navigate to the alert visit {}".
                format(self.item.url, "http://pricing.jslvtr.com/alerts/{}".format(self._id))
            }
        )

    @classmethod
    def find_need_update(cls, minutes_since_update = AlertConstants.ALERT_TIMEOUT):
        last_update_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes = minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {
                                                          "last_checked":
                                                           {"$lte": last_update_limit}, "is_active": True}

                                                      )]


    def json(self):
        # return json representation of the object
        return {
            '_id': self._id,
            'user_email': self.user_email,
            'price_limit': self.price_limit,
            'item_id': self.item_id,
            'last_checked': self.last_checked,
            'is_active': self.is_active
        }


    def save_to_mongo(self):
        # pass the alert to mongoDb
        #instead insert data - we may need to update existing one = check by ID and decide if to insert or update
        # Database.insert(AlertConstants.COLLECTION, self.json())
        Database.update(AlertConstants.COLLECTION, {'_id': self._id}, self.json())


    def load_item_price(self):
        if not self.is_active:
            raise AlertErrors.AlertNotActiveError("Your alert is not active - can't update price")
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        # need to update again the alert into the DB and also the item price
        self.save_to_mongo()
        self.item.save_to_mongo()
        return self.item.price


    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            status = self.send()
            print(status)

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': user_email})]


    @classmethod
    def get_by_id(cls, _id):
        alert_data = Database.find_one(AlertConstants.COLLECTION, {'_id': _id})
        if alert_data == None:
            return None
        else:
            return cls(**alert_data)


    def deactivate(self):
        """
        update the status to active
        :return: indication if status was updated and saved in DB
        """
        if self.is_active:
            self.is_active = False
            self.save_to_mongo()
            return True
        else:
            return False


    def activate(self):
        """
        update the status to in-active
        :return: indication if status was updated and saved in DB
        """
        if not self.is_active:
            self.is_active = True
            self.save_to_mongo()
            return True
        else:
            return False


    def remove_from_mongo(self):
        # remove the alert from mongoDb
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})


    @classmethod
    def get_alerts(cls):
        return [cls(**alert) for alert in Database.find(AlertConstants.COLLECTION, {})]