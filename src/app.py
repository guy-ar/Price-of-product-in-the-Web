from flask import Flask, render_template

from src import config
from src.common.database import Database

app = Flask(__name__)

#load the configuration to the app by creating the member from object
app.config.from_object('config')
app.secret_key = 'test'

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.html')

# register all blue prints
from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix = "/users")

from src.models.alerts.views import alert_blueprint
app.register_blueprint(alert_blueprint, url_prefix = "/alerts")

from src.models.stores.views import store_blueprint
app.register_blueprint(store_blueprint, url_prefix = "/stores")

