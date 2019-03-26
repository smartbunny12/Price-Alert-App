from flask import Flask, render_template

from scr.common.database import Database




app = Flask(__name__)
app.config.from_object('config')

app.secret_key ='123'


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')

from scr.models.users.views import user_buleprint
from scr.models.alerts.views import alert_blueprint
from scr.models.stores.views import store_buleprint
# register the blue[print with prefix users
app.register_blueprint(user_buleprint, url_prefix = '/users')
app.register_blueprint(store_buleprint, url_prefix = '/stores')
app.register_blueprint(alert_blueprint, url_prefix = '/alerts')



