import requests
import json
import pprint
import re
import wiki_template

def get_page(lang, page):
    return requests.get('http://'+lang+'.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=' + page.strip()).content

def pretty(code):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(code)

def get_first(d):
    return d[list(d.keys())[0]]

def get_infobox(page): # Returns infobox
    isInfobox = lambda template: wiki_template.parse_template(template)['template_name'].lower().startswith('infobox')
    infoboxes = list(filter(isInfobox, wiki_template.get_templates_on_page(page)))
    if len(infoboxes) == 0:
        return ''
    infobox = infoboxes[0]
    return infobox

def has_infobox(page, infobox_type):
    infobox = get_infobox(page)
    actual_infobox_category = wiki_template.parse_template(infobox)['template_name']
    if (infobox == '') or (re.search(r'infobox\s+' + infobox_type.lower(), actual_infobox_category.lower()) == None):
        return False
    else:
        return True


def parse_link(template): # returns [Link_Title, Description] or [Link_Title]
    start = template.find('[[')
    finish = template.find(']]')
    return template[start+2:finish].split('|')

def parse_date(template):
    result = []

    template = template.lower().replace('&nbsp;', ' ')
    
    if re.search(r'\d{1,4}\sbc', template):
        groups = list(map(lambda t: t.groups()[0], re.finditer(r'(\d{1,4})\sbc', template)))
        years = list(map(int, groups))
        year_start = max(years)
        year_end = min(years)
        return ([1, 1, -year_start], [31, 12, -year_end])
    
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

    dashes = r'[\u2012\u2013\u2014\u2015-]'
    month_regexp = r'january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec'

    t = re.search(r'(' + month_regexp + r')\s(\d{3,4})\s?' + dashes + r'\s?(' + month_regexp + r')\s(\d{3,4})', template)
    if t:
        t = t.groups()
        return ([1, month[t[0]], int(t[1])], [1, month[t[2]], int(t[3])])
    
    t = re.search(r'(' + month_regexp + r')\s(\d{1,2})\s?' + dashes + r'\s?(' + month_regexp + r')\s(\d{1,2}),\s(\d{3,4})', template)
    if t:
        t = t.groups()
        return ([int(t[1]), month[t[0]], int(t[4])], [int(t[3]), month[t[2]], int(t[4])])
    
    t = re.search(r'(\d\d)\s*'+dashes+r'\s*(\d\d)\s+(' + month_regexp + r')\s*,?\s*(\d{3,4})', template)
    if t:
        t = t.groups()
        return ([int(t[0]), month[t[2]], int(t[3])], [int(t[1]), month[t[2]], int(t[3])])

    t = re.search(r'(' + month_regexp + r')\s+(\d\d)' + dashes + r'(\d\d),?\s*(\d{3,4})', template)
    if t:
        t = t.groups()
        return ([int(t[1]), month[t[0]], int(t[3])], [int(t[2]), month[t[0]], int(t[3])])

    t = re.search(r'('+month_regexp + r')\s*' + dashes + r'\s*(' + month_regexp + r')\s+(\d{3,4})', template)
    if t:
        t = t.groups()
        return ([1, month[t[0]], int(t[2])], [1, month[t[1]], int(t[2])])

    t = re.search(r'(\d+)\s+(' + month_regexp + r'),?\s*(\d+)', template)
    if t:
        t = t.groups()
        return ([int(t[0]), month[t[1]], int(t[2])], [int(t[0]), month[t[1]], int(t[2])])

    t = re.search(r'(' + month_regexp + r')\s+(\d+),?\s*(\d+)', template)
    if t:
        t = t.groups()
        return ([int(t[1]), month[t[0]], int(t[2])], [int(t[1]), month[t[0]], int(t[2])])

    t = re.search(r'(\d+)\s+(' + month_regexp + r'),?\s*(\d+)', template)
    if t:
        t.groups()
        return ([int(t[0]), month[t[1]], int(t[2])], [int(t[0]), month[t[1]], int(t[2])])

    t = re.search(r'(' + month_regexp + r')\s+(\d+),?\s*(\d+)', template)
    if t:
        t = t.groups()
        return ([int(t[1]), month[t[0]], int(t[2])], [int(t[1]), month[t[0]], int(t[2])])

    t = re.search(r'\s*(\d{3,4})\s*' + dashes + r'\s*(\d{3,4})\s*', template)
    if t:
        t = t.groups()
        return ([1, 1, int(t[0])], [1, 1, int(t[1])])

    t = re.search(r'\s*(\d{3,4})\s*' + dashes + r'\s*(\d\d)\s*', template)
    if t:
        t = t.groups()
        return ([1, 1, int(t[0])], [1, 1, int(t[0][0:2]+t[1])])
    # re.match(r'(\d+)\s+(january|february|march|april|may|june|july|august|september|november|december)')

    t = re.search(r'\s*(\d{3,4})\s*', template)
    if t:
        t = t.groups()
        return ([1, 1, int(t[0])], [1, 12, int(t[0])])

    return result


def parse_birth_date_template(template):
    t = re.search(r'(\d+)\|(\d+)\|(\d+)', template)
    if t:
        t = t.groups()
        t = tuple(map(int, t))
        return (t[2], t[1], t[0])


def parse_death_date_template(template):
    return parse_birth_date_template(template)


def regex_ok(ex, s):
    return re.search(ex, s) != None


def parse_combatant_template(template):
    template = template.lower()
    #print(template)
    dashes = r'\u2012\u2013\u2014\u2015-'
    t = re.search(r'[\[\{](flag|flagcountry|flagicon|flag icon|flagu|army|navy)\|([\w\s\(\),'+dashes+r']+)[\|\}\]]', template)
    if t:
        t = t.groups()
        if len(t) > 1:
            return t[1]
    t = re.search(r'[\[\{]([\w\s(\),'+dashes+r']+)[\|\}\]]', template)
    if t:
        t = t.groups()
        if len(t) > 0:
            return t[0]
    return ''


def parse_place_template(template):
    dashes = r'\u2012\u2013\u2014\u2015-'
    return re.findall(r'\[\[([\w\s(\),'+dashes+r']+)\]\]', template) + re.findall(r'\|([\w\s(\),'+dashes+r']+)\]\]', template)


def parse_infobox_military_conflict(page):
    parsed_template = wiki_template.parse_template(page)['options']
    result = {}
    if 'conflict' in parsed_template:
        result['conflict'] = parsed_template['conflict']
    if 'date' in parsed_template:
        result['date'] = parse_date(parsed_template['date'])
    if 'place' in parsed_template:
        result['place'] = ', '.join(parse_place_template(parsed_template['place']))
    if 'partof' in parsed_template:
        pl = parse_link(parsed_template['partof'])
        if len(pl) == 2:
            result['partof'] = {'link': pl[0], 'description': pl[1]}
        elif len(pl) == 1:
            result['partof'] = {'link': pl[0]}
    combatants = []

    for s1 in ['1', '2', '3']:
        for s2 in ['', 'a', 'b', 'c', 'd']:
            cmb = 'combatant' + s1 + s2
            if cmb in parsed_template:
                combatants.append(parse_combatant_template(parsed_template[cmb]))
    if len(combatants) > 0:
        result['combatants'] = combatants
    return result

def parse_list_template(template):
    res = []
    for s in re.findall(r'\[\[[^\]]+\]\]', template):
        res.append(s[2:len(s)-2])
    return res

def parse_infobox_scientist(page):
    # return wiki_template.parse_template(page)['options']
    parsed_template = wiki_template.parse_template(page)['options']
    result = {
        'name'       : parsed_template['name'],
        'birth_date' : parsed_template['birth_date'],
        'death_date' : parsed_template['death_date'],
        'fields'     : parsed_template['fields'],
    }
    return result
