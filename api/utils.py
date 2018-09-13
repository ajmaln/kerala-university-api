from bs4 import BeautifulSoup
import json
import requests


URLS = {
    'results': "https://exams.keralauniversity.ac.in/Login/check8",
    'notifications': "https://exams.keralauniversity.ac.in/Login/check1",
}

def link_and_text(each):
    link = each.find('a', href=True)
    if(link):
        return {
            'title': each.text.strip(),
            'link': link['href']
        }


def scrap_data(url_name):
    page = requests.get(URLS[url_name])
    parsed = BeautifulSoup(page.content, 'html.parser')
    data = filter(lambda x: x!=None, map(link_and_text, parsed.find_all('tr')))
    return json.dumps(list(data)[1:-1])