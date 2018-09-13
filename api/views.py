from django.shortcuts import render
from django.http import HttpResponse
from .models import Data
from .utils import scrap_data


def generic_view(request=None, scrap=False, url_name=''):
    try:
        if url_name == '':
            raise Exception('url_name cannot be empty')
        json_data = Data.objects.filter(type=url_name).latest().json_data
        if scrap:
            json_data = scrap_data(url_name)

        if request:
            response = HttpResponse(json_data, status=200, content_type='application/json')
            response["Access-Control-Allow-Origin"] = "*"
            return response
        else:
            return json_data
    except Data.DoesNotExist:
        json_data = scrap_data(url_name);
        if request:
            response = HttpResponse(json_data, status=200, content_type='application/json')
            response["Access-Control-Allow-Origin"] = "*"
            return response
        else:
            return json_data


def results_view(request=None, scrap=False):
    return generic_view(request, scrap, url_name='results')

def notifications_view(request=None, scrap=False):
    return generic_view(request, scrap, url_name='notifications')

