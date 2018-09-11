from firebase_admin import messaging
from KeralaUniversityApi.firebase import db
import os
import environ
import requests
import json

root = environ.Path(__file__) - 1
env = environ.Env()

def get_tokens():
    docs = db.collection('tokens').get()
    tokens = map(lambda x: x.id, docs)
    # return list(map(lambda x: x.to_dict(), docs))
    return tokens


def send_message(message):
    messaging.Message({
        'message': 'hey bro!'
    }, token='')

api_headers = {
    'Authorization': "key={}".format(env('API_KEY'))
}

def get_details(token):
    resp = requests.get('https://iid.googleapis.com/iid/info/{token}?details=true'.format(token=token), 
        headers=api_headers
    )
    return json.loads(resp.content)


def subscribe_to(topic, token):
    resp = requests.post('https://iid.googleapis.com/iid/v1/{token}/rel/topics/{topic}'.format(token=token, topic=topic), 
        headers=api_headers
    )
    print(resp.content)




