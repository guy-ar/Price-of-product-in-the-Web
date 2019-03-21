from flask import Blueprint, render_template, request, session, make_response, url_for, redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators
import src.models.stores.error as StoreErrors

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route("/")
def index():
    alerts = Alert.get_alerts()
    return render_template('alerts/alert_index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['POST', 'GET'])
@user_decorators.requires_login
# add new decorator that will be in charge for validating if user is already logged in
# if not it will redirect it to login page
def create_alert():

    # in case we receive GET - this is the first time the page is opened
    # in case we receive  POST - we have the details
    if request.method == 'GET':
        return render_template('alerts/create_alert.html')
    else:
        # get from the request the newly created alert details
        price_limit = float(request.form['price_limit'])
        item_name = request.form['name']
        item_url = request.form['url']
        try:
            item = Item(item_name, item_url)
        except StoreErrors.StoreError as e:
            return e.message
        #get the user details from DB by session email
        user_email = session['email']

        # create the new blog in DB
        new_alert = Alert(user_email, price_limit, item._id)

        new_alert.load_item_price()


        # save to DB only after alert was created
        item.save_to_mongo()

        # will prepare the data of existing alert - based on above method
        return make_response(get_alert_page(new_alert._id))



@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    alert.deactivate()
    #redirect to the next entry point
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    status_update = alert.activate()
    # if it is reactivated - need to update also the price
    if status_update:
        alert.load_item_price()
    #redirect to the next entry point
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.get_by_id(alert_id)
    return render_template('alerts/alert.html', alert=alert)

@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass

@alert_blueprint.route('check_price/<string:alert_id>')
@user_decorators.requires_login
def check_alert_price(alert_id):
    alert = Alert.get_by_id(alert_id)
    alert.load_item_price()
    # we have end entry point that present the item and we need to redirect to it
    # pay attentuion that this method is in current view - therefore it start with '.'
    return redirect(url_for('.get_alert_page', alert_id=alert._id))

@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    alert.remove_from_mongo()
    #redirect to the next entry point
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/update/<string:alert_id>', methods=['POST', 'GET'])
@user_decorators.requires_login
# add new decorator that will be in charge for validating if user is already logged in
# if not it will redirect it to login page
def update_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    item = Item.get_by_id(alert.item._id)
    # in case we receive GET - this is the first time the page is opened
    # in case we receive  POST - we have the details
    if request.method == 'GET':
        return render_template('alerts/edit_alert.html', alert=alert)
    else:
        # get from the request the newly created alert details
        price_limit = float(request.form['price_limit'])

        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('users.user_alerts'))
