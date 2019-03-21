

from flask import Blueprint, render_template, request, make_response, url_for, redirect, json
import src.models.users.decorators as user_decorators
from src.models.stores.store import Store

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route("/")
def index():
    stores = Store.get_stores()
    return render_template('stores/store_index.html', stores=stores)



@store_blueprint.route('/new', methods=['POST', 'GET'])
@user_decorators.requires_admin_priv
def create_store():

    # in case we receive GET - this is the first time the page is opened
    # in case we receive  POST - we have the details
    if request.method == 'GET':
        return render_template('stores/create_store.html')
    else:
        # get from the request the newly created alert details
        name = request.form['name']
        url_prefix = request.form['url']
        tag_name = request.form['tag_name']
        # need to format the query as json
        query = json.load(request.form['query'])

        store = Store(name, url_prefix, tag_name, query)

        store.save_to_mongo()

        return redirect(url_for('stores.index'))


@store_blueprint.route('/<string:store_id>')
def get_store_page(store_id):
    store = Store.get_by_id(store_id)
    return render_template('stores/store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin_priv
def delete_store(store_id):
    store = Store.get_by_id(store_id)
    store.remove_from_mongo()
    #redirect to the next entry point
    return redirect(url_for('stores.index'))


@store_blueprint.route('/update/<string:store_id>', methods=['POST', 'GET'])
@user_decorators.requires_admin_priv
def update_store(store_id):
    # in case we receive GET - this is the first time the page is opened
    # in case we receive  POST - we have the details
    store = Store.get_by_id(store_id)
    if request.method == 'GET':
        return render_template('stores/edit_store.html', store=store)
    else:
        # get from the request the newly created alert details
        name = request.form['name']
        url_prefix = request.form['url']
        tag_name = request.form['tag_name']
        query = request.form['query']

        # upload from DB the store details and then set them with new data

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query
        store.save_to_mongo()
        return redirect(url_for('stores.index'))