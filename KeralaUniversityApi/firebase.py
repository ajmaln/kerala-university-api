import firebase_admin
from firebase_admin import credentials, firestore
import json
import environ

root = environ.Path(__file__) - 1
env = environ.Env()
service_account = json.loads(env('SERVICE_ACCOUNT'))
service_account['private_key'] = bytes(service_account['private_key'], "utf-8").decode("unicode_escape")

cred = credentials.Certificate(service_account)
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()