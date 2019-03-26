from flask import Blueprint, render_template, request, session, url_for, redirect

from scr.models.alerts.alert import Alert
from scr.models.items.item import Item

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/')
def index():
    return "This is the alerts index"

@alert_blueprint.route('/new', methods=['GET', 'POST'])
def create_alert():
    if request.method == 'POST':
        name=request.form['name']
        url = request.form['url']
        price_limit =request.form['price_limit']

        item = Item(name, url)
        item.save_to_mongo()

        alert= Alert(session['email'], price_limit, item._id)
        alert.load_item_price() # already save to db

    return render_template('alerts/new_alert.html')



@alert_blueprint.route('/deactivate/alert_id' )
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/activate/alert_id' )
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/alert/<string:alert_id>')
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html')



@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
