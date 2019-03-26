from scr.common.database import Database
from scr.models.alerts.alert import Alert


Database.initialize()
# find the alters that nneds to update and send the email if the price has reached
alerts_needing_update = Alert.find_needing_update()

for alert in alerts_needing_update:
    alert.load_item_price()
    alert.send_email_if_price_reached()