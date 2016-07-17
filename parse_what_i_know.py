import wikilib
import categoryLister as lister
import subprocess

def get_coord(page):
    process = subprocess.Popen(['perl', 'coorder.pl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return process.communicate(input=page.encode('UTF-8'))[0].strip()

def has_coord(page):
    return get_coord(page) != b''

def parse(page):
    res = wikilib.parse_infobox_military_conflict(wikilib.get_infobox(page)[0])
    return (res != '') and ('date' in res) and has_coord(page)

def main():
    f = open('logs/page_list.txt')
    lst = f.readlines()
    for s in lst:
        s = s.strip()
        if parse(lister.cachingGetPage(s)):
            print(s)

if __name__ == '__main__':
    main()
