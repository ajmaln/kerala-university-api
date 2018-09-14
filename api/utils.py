from bs4 import BeautifulSoup
import json
import requests


URLS = {
    'results': "https://exams.keralauniversity.ac.in/Login/check8",
    'notifications': "https://exams.keralauniversity.ac.in/Login/check1",
}


def find_until_table_heading(tag, date, text_list=[]):
    if tag.has_attr('class') and tag['class'][0] == 'tableHeading':
        return {date: text_list}
    else:
        if tag.find('a', href=True) and not tag.text.strip().startswith('<<'):
            text_list.append({'title': tag.text.strip(),
                              'link': tag.find('a', href=True)['href']})
        if tag.findNext('tr'):
            return find_until_table_heading(tag.findNext('tr'), date, text_list)
        return {date: text_list}


def link_and_text(each):
    date = each.text[-10:]
    data = find_until_table_heading(each.findNext('tr'), date, [])
    return data


def scrap_data(url_name):
    page = requests.get(URLS[url_name])
    parsed = BeautifulSoup(page.content, 'html.parser')
    data = filter(lambda x: x != None, map(
        link_and_text, parsed.find_all('tr', class_='tableHeading')))
    return json.dumps(list(data))
