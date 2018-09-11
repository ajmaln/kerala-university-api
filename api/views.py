from django.shortcuts import render
from django.http import HttpResponse

from .models import Data

from bs4 import BeautifulSoup
import requests
import json
from .fcm import get_details

# Create your views here.

def link_and_text(each):
    if(each.find('a', href=True)):

        return {
            'title': each.text.strip(),
            'link': each.find('a')['href']
        }


def scrap_data():
    page = requests.get("https://exams.keralauniversity.ac.in/Login/check8")
    parsed = BeautifulSoup(page.content, 'html.parser')
    data = filter(lambda x: x!=None, map(link_and_text, parsed.find_all('tr')))
    return json.dumps(list(data)[1:-1])


def results_view(request=None, scrap=False):
    try:
        json_data = Data.objects.filter(type='results').latest().json_data
        if scrap:
            json_data = scrap_data()

        if request:
            response = HttpResponse(json_data, status=200, content_type='application/json')
            response["Access-Control-Allow-Origin"] = "*"
            return response
        else:
            return json_data
    except Data.DoesNotExist:
        json_data = scrap_data();
        if request:
            response = HttpResponse(json_data, status=200, content_type='application/json')
            response["Access-Control-Allow-Origin"] = "*"
            return response
        else:
            return json_data


def scan_for_change(request=None):
    # Fetch and parse webpage
    old_data = Data.objects.latest()
    new_data = results_view()

    # Analyze for change
    if old_data:
        if not old_data.json_data == new_data:
            old_data.json_data = new_data
            old_data.save()
    else:
        Data.objects.create(json_data=new_data)


    # Notify if changed
    # Notification Logic


