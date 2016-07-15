import wikilib
import categoryLister as lister
import subprocess


def has_coord(page):
    process = subprocess.Popen(['perl coorder.pl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print(process.communicate(input=page.encode('UTF-8')))
    return True
    #return process.communicate(input=page)[0] != ''


def parse(page):
    res = wikilib.parse_infobox_military_conflict(wikilib.get_infobox(page)[0])
    return (res != '') and ('date' in res) and has_coord(page)

f = open('logs/page_list.txt')
lst = f.readlines()
for s in lst:
    s = s.strip()
    if parse(lister.cachingGetPage(s)):
        print(s)
