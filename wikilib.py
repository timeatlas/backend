import requests
import json
import pprint

def get_page(lang, page):
    return requests.get('http://'+lang+'.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=' + page.strip()).content

def pretty(code):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(code)

def get_first(d):
    return d[list(d.keys())[0]]

def get_infobox(page):
    infobox = ''
    balance = 0
    j = 0
    while page[j:j+9].lower() != '{{infobox':
        j += 1
    for i in range(j, len(page)):
        if page[i] == '{':
            balance += 1
        elif page[i] == '}':
            balance -= 1
        if balance == 0:
            infobox = page[j:i+1]
            break
    return infobox

def has_infobox(page):
    return get_infobox(page) != ''

def parse_link(template): # returns [Link_Title, Description] or [Link_Title]
    start = template.find('[[')
    finish = template.find(']]')
    return template[start+2:finish].split('|')

def parse_date(template):
    result = {}
    template = template.lower()
    month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
             'september', 'november', 'december']
    for i in range(len(month)):
        if month[i] in template:
            result['month'] = i + 1
            start = template.find(month[i])
            while not template[start].isdigit():
                start += 1
            finish = start
            while template[finish].isdigit():
                finish += 1

    # September 2012

def parse_infobox_military_conflict(page):
    result = {}
    page = page.split('\n')
    for s in page:
        s = s.split('=')
        if s[0] == '|conflict':
            result['conflict'] = s[1]
        elif s[0] == '|partof':
            pl = parse_link(s[1])
            if len(pl) == 2:
                result['partof'] = {'link': pl[0], 'description': pl[1]}
            elif len(pl) == 1:
                result['partof'] = {'link': pl[0]}
        elif s[0] == '|date':
            result['date'] = s[1]
        elif s[0] == '|place':
            result['place'] = parse_link(s[1])

    return result