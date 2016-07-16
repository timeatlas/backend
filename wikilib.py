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

def get_infobox(page): # Returns (infobox, type)
    infobox = ''
    balance = 0
    start_info = 0
    while page[start_info:start_info+9].lower() != '{{infobox':
        if start_info + 9 >= len(page):
            return ''
        start_info += 1
    finish_tp = start_info + 10
    while page[finish_tp] != '|':
        finish_tp += 1
    infobox_type = page[start_info+10:finish_tp]
    for i in range(start_info, len(page)):
        if page[i] == '{':
            balance += 1
        elif page[i] == '}':
            balance -= 1
        if balance == 0:
            infobox = page[start_info:i+1]
            break
    return (infobox, infobox_type.strip())

def has_infobox(page, type):
    box = get_infobox(page)
    if (box == '') or (box[1].lower() != type.lower()):
        return False
    else:
        return True


def parse_link(template): # returns [Link_Title, Description] or [Link_Title]
    start = template.find('[[')
    finish = template.find(']]')
    return template[start+2:finish].split('|')

def parse_date(template):
    #print('date template:', template)
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

    dashes = r'\u2012\u2013\u2014\u2015'
    month_regexp = r'january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec'

    t = re.search(r'(\d+)\s+(' + month_regexp + r'),?\s*(\d+)', template)
    #print(t)
    # Date: dd/mm/yyyy
    if t:
        t = t.groups()
        return ([int(t[0]), month[t[1]] + 1, int(t[2])], [int(t[0]), month[t[1]] + 1, int(t[2])])

    t = re.search(r'(' + month_regexp + r')\s+(\d+),?\s*(\d+)', template)
    #print(t)
    if t:
        t = t.groups()
        return ([int(t[1]), month[t[0]] + 1, int(t[2])], [int(t[1]), month[t[0]] + 1, int(t[2])])

    t = re.search(r'(\d+)\s+(' + month_regexp + r'),?\s*(\d+)', template)
    #print(t)
    # Date: dd/mm/yyyy
    if t:
        t.groups()
        return ([int(t[0]), month[t[1]] + 1, int(t[2])], [int(t[0]), month[t[1]] + 1, int(t[2])])

    t = re.search(r'(' + month_regexp + r')\s+(\d+),?\s*(\d+)', template)
    #print(t)
    if t:
        t = t.groups()
        return ([int(t[1]), month[t[0]] + 1, int(t[2])], [int(t[1]), month[t[0]] + 1, int(t[2])])

    t = re.search(r'\s*(\d\d\d\d)\s*[' + dashes + r']\s*(\d\d\d\d)\s*', template)
    #print(t)
    if t:
        t = t.groups()
        return ([1, 1, int(t[0])], [1, 1, int(t[1])])

    t = re.search(r'\s*(\d\d\d\d)\s*[' + dashes + r']\s*(\d\d)\s*', template)
    #print(t)
    if t:
        t = t.groups()
        return ([1, 1, int(t[0])], [1, 1, int(t[0][0:2]+t[1])])
    # re.match(r'(\d+)\s+(january|february|march|april|may|june|july|august|september|november|december)')
    return result

def parse_birth_date_template(template):
    t = re.search(r'(\d+)\|(\d+)\|(\d+)', template)
    # print(t)
    # Date: dd/mm/yyyy
    if t:
        t = t.groups()
        t = tuple(map(int, t))
        return (t[2], t[1], t[0])


def parse_death_date_template(template):
    return parse_birth_date_template(template)


def regex_ok(ex, s):
    return re.search(ex, s) != None


def parse_infobox_military_conflict(page):
    result = {}
    page = page.split('\n')
    for s in page:
        s = s.partition('=')
        if len(s) == 3:
            s = (s[0].strip(), s[2].strip())
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


def parse_list_template(template):
    res = []
    for s in re.findall(r'\[\[[^\]]+\]\]', template):
        res.append(s[2:len(s)-2])
    return res


def parse_infobox_scientist(page):
    result = {}
    page = page.split('\n')
    for s in page:
        s = s.partition('=')
        if len(s) == 3:
            s = (s[0].strip(), s[2].strip())
        if regex_ok('\|\s*name', s[0]):
            print(s)
            result['name'] = s[1]
        elif regex_ok('\|\s*birth_date', s[0]):
            print(s)
            result['birth_date'] = parse_birth_date_template(s[1])
        elif regex_ok('\|\s*death_date', s[0]):
            print(s)
            result['death_date'] = parse_death_date_template(s[1])
        elif regex_ok('\|\s*fields', s[0]):
            result['fields'] = parse_list_template(s[1])

    return result
