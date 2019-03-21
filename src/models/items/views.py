from flask import Blueprint

item_bluprint = Blueprint('items', __name__)

@item_bluprint.route('item/<string:name>')
def item_page(name):
    pass


