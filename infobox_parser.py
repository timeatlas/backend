from wikilib import *
from categoryLister import cachingGetPage

def get_place():
    f = open('logs/page_list.txt')
    lst = f.readlines()
    for s in lst:
        s = s.strip()
        #page = get_page('en', s)
        page = cachingGetPage(s)
        #js = json.loads(page.decode('UTF-8'), encoding='UTF-8')
        try:
            content = get_infobox(page).split('\n')
            for s1 in content:
                s1 = s1.split('=')
                if regex_ok(r'\|\s+'):
                    print(s1[1])
        except:
            pass

if __name__ == '__main__':
    #get_place()
    """input('Введите название страницы:\n'"""
    page = get_page('en', 'Italian_War_of_1521–26')
    js = json.loads(page.decode('UTF-8'), encoding='UTF-8')
    content = get_infobox(get_first(js['query']['pages'])['revisions'][0]['*'])
    print(wiki_template.parse_template(content)['options'])
    print(parse_infobox_military_conflict(content))
    #print('_=###########################')
    #print(get_infobox(content))
    #print('#################')
    #print(has_infobox(content, 'military conflict'))
    #page = cachingGetPage('Albert_Einstein')
    #print(parse_infobox_scientist(get_infobox(page)))


