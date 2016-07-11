import requests
import json
import pprint
import re

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
        if j + 9 == len(page):
            return ''
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
    print('date template:', template)
    result = []
    """template = template.lower()
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
                finish += 1"""

    template = template.lower()
    month = {'january': 1, 'jan': 1,
             'february': 2, 'feb': 2,
             'march': 3,  'mar': 3,
             'april': 4, 'apr': 4,
             'may': 5,
             'june': 6, 'jun': 6,
             'july': 7, 'jul': 7,
             'august': 8, 'aug': 8,
             'september': 9, 'sep': 9,
             'october': 10, 'oct': 10,
             'november': 11, 'nov': 11,
             'december': 12, 'dec': 12}

    t = re.findall(r'(\d+)\s+(january|february|march|april|may|june|july|august|september|october|november|december),\s*(\d+)', template)
    print(t)
    # Date: dd/mm/yyyy
    if t:
        return ([int(t[0][0]), month[t[0][1]] + 1, int(t[0][2])], [int(t[0][0]), month[t[0][1]] + 1, int(t[0][2])])

    t = re.findall(r'(january|february|march|april|may|june|july|august|september|oct|november|december)\s+(\d+),\s*(\d+)', template)
    print(t)
    if t:
        return ([int(t[0][1]), month[t[0][0]] + 1, int(t[0][2])], [int(t[0][1]), month[t[0][0]] + 1, int(t[0][2])])

    t = re.findall(r'(\d+)\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec),\s*(\d+)', template)
    print(t)
    # Date: dd/mm/yyyy
    if t:
        return ([int(t[0][0]), month[t[0][1]] + 1, int(t[0][2])], [int(t[0][0]), month[t[0][1]] + 1, int(t[0][2])])

    t = re.findall(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec)\s+(\d+),\s*(\d+)', template)
    print(t)
    if t:
        return ([int(t[0][1]), month[t[0][0]] + 1, int(t[0][2])], [int(t[0][1]), month[t[0][0]] + 1, int(t[0][2])])

    t = re.findall(r'\s*(\d\d\d\d)\s*[\u2012\u2013\u2014\u2015]\s*(\d\d\d\d)\s*', template)
    print(t)
    if t:
        return ([1, 1, t[0][0]], [1, 1, t[0][1]])

    t = re.findall(r'\s*(\d\d\d\d)\s*[\u2012\u2013\u2014\u2015]\s*(\d\d)\s*', template)
    print(t)
    if t:
        return ([1, 1, t[0][0]], [1, 1, t[0][0][0:3]+t[0][1]])
    # re.match(r'(\d+)\s+(january|february|march|april|may|june|july|august|september|november|december)')
    return result

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
            result['date'] = parse_date(s[1])
        elif s[0] == '|place':
            result['place'] = parse_link(s[1])

    return result