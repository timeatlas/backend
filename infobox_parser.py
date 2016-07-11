from wikilib import *

if __name__ == '__main__':
    """input('Введите название страницы:\n'"""
    page = get_page('en', 'Battle_of_Kulikovo')
    js = json.loads(page.decode('UTF-8'), encoding='UTF-8')
    content = get_first(js['query']['pages'])['revisions'][0]['*']
    print(content)
    print(parse_infobox_military_conflict(content))
    print('_=###########################')
    #print(get_infobox(content))

