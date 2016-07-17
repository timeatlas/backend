import urllib.request
import urllib.parse
import urllib.error
import wikilib
import sys
import os.path
import json
import copy
import re

BASE = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmlimit=500&format=json'
PAGE_BASE = 'https://en.wikipedia.org/w/index.php?title='
SUMMARY_BASE='https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='

def pagesList(categoryName, cmtype='page'):
    req = BASE + '&' + urllib.parse.urlencode({'cmtitle': categoryName, 'cmtype': cmtype})
    res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    members = res['query']['categorymembers']
    while 'continue' in res:
        cReq = req + '&cmcontinue=' + res['continue']['cmcontinue']
        res = json.loads(urllib.request.urlopen(cReq).read().decode('utf-8'))
        members += res['query']['categorymembers']
    return members

def subcategoriesList(categoryName):
    return pagesList(categoryName, cmtype='subcat')

def cachingGetPage(pageName):
    pageFileName = urllib.parse.urlencode({'': pageName})[1:]
    filename = os.path.join('pagesCache', '{}.cached'.format(pageFileName))
    if os.path.isfile(filename):
        f = open(filename, encoding='utf-8')
        res = f.read()
        f.close()
        return res
    else:
        pageUrl = PAGE_BASE + urllib.parse.urlencode({'': pageName.replace(' ','_')})[1:] + '&action=raw'
        try:
            res = urllib.request.urlopen(pageUrl).read().decode('utf-8')
        except urllib.error.HTTPError:
            res = ''
        if res.startswith('#REDIRECT '):
            realName = re.search(r'#REDIRECT\s\[\[(.*?)\]\]', res)
            realName = realName.groups()[0]
            return cachingGetPage(realName)
        f = open(filename, 'w', encoding='utf-8')
        f.write(res)
        f.close()
        return res

def cachingGetSummary(pageName):
    summaryFileName = urllib.parse.urlencode({'': pageName})[1:]
    filename = os.path.join('summaryCache', '{}.cached'.format(summaryFileName))
    if os.path.isfile(filename):
        f = open(filename, encoding='utf-8')
        res = f.read()
        f.close()
        return res
    else:
        pageUrl = SUMMARY_BASE + summaryFileName
        res = urllib.request.urlopen(pageUrl).read().decode('utf-8')
        res = list(json.loads(res)['query']['pages'].values())[0]['extract']
        f = open(filename, 'w', encoding='utf-8')
        f.write(res)
        f.close()
        return res

def recursivePagesList(categoryName, lim=-1, testF=(lambda _: True), used=set(), path=[], fullPath=False, logFile=None):
    used.add(categoryName)
    path = path + [categoryName]
    if lim == 0:
        return []
    memberCandidates = pagesList(categoryName)
    members = []
    for page in memberCandidates:
        if page['title'] not in used:
            used.add(page['title'])
            pageTxt = cachingGetPage(page['title'])
            if testF(pageTxt):
                if fullPath:
                    members.append(tuple(path) + (page['title'],))
                    print(members[-1], flush=True)
                else:
                    members.append(page['title'])
                    print(members[-1], flush=True)
    for cat in subcategoriesList(categoryName):
        if cat['title'] not in used:
            print('Going level down to ' + cat['title'], file=sys.stderr)
            title = cat['title'].replace(' ', '_')
            members += recursivePagesList(title, lim=lim - 1, testF=testF, used=used, path=path, fullPath=fullPath)
    return members

def categoryList(name, outFile=sys.stdout, fullPath=False, testF=(lambda _: True), lim=-1):
    for page in recursivePagesList(name, fullPath=fullPath, testF=testF, lim=lim):
        if type(page) == str:
            print(page, file=outFile)
        else:
            print(' -> '.join(page), file=outFile)

def main():
    print('Enter category name:', end=' ', file=sys.stderr)
    categoryName = 'Category:' + input()
    print('Display full paths? (Y/N)?', end=' ', file=sys.stderr)
    fullPath = (input().upper() == 'Y')
    filename = os.path.join('logs', '{}.log'.format(categoryName))
    with open(filename, 'w') as f:
        with open('logs/page_list.txt','w', encoding='utf-8') as outFile:
            old_stdout = sys.stdout
            sys.stdout = outFile
            testF = lambda page: wikilib.has_infobox(page, 'military conflict')
            categoryList(categoryName.replace(' ', '_'), fullPath=fullPath, outFile=f, testF=testF)
            sys.stdout = old_stdout


if __name__ == '__main__':
    main()
