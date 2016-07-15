import wikilib
import categoryLister as lister

def get_place():
    f = open('logs/page_list.txt')
    lst = f.readlines()
    for s in lst:
        s = s.strip()
        #page = get_page('en', s)
        page = lister.cachingGetPage(s)
        #js = json.loads(page.decode('UTF-8'), encoding='UTF-8')
        try:
            content = wikilib.get_infobox(page)[0].split('\n')
            for s1 in content:
                s1 = s1.split('=')
                if s1[0] == '|place':
                    print(s1[1])
        except:
            pass