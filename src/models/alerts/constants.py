import os

COLLECTION = "Alerts"

URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('MAILGUN_API_KEY')

FROM = os.environ.get('MAOLGUN_SANDBOX_SENDER')
ALERT_TIMEOUT = 1
