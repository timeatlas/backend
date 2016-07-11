import urllib.request
import urllib.parse
import urllib.error
import sys
import json

BASE = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmlimit=500&format=json'
PAGE_BASE = 'https://en.wikipedia.org/w/index.php?title='

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

def recursivePagesList(categoryName, lim=-1, testF=(lambda _: True), used=set(), path=[], fullPath=False):
	used.add(categoryName)
	path = path + [categoryName]
	if lim == 0:
		return []
	memberCandidates = pagesList(categoryName)
	members = []
	for page in memberCandidates:
		if page['title'] not in used:
			used.add(page['title'])
			pageUrl = PAGE_BASE + urllib.parse.urlencode({'':page['title'].replace(' ','_')})[1:] + '&action=raw'
			try:
				pageTxt = urllib.request.urlopen(pageUrl).read().decode('utf-8')
			except urllib.error.HTTPError:
				pageTxt = ''
			if testF(pageTxt):
				if fullPath:
					members.append(tuple(path) + (page['title'],))
					print(members[-1])
				else:
					members.append(page['title'])
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
	categoryName = 'Category:' + input('Enter category name: ')
	fullPath = (input('Display full paths (Y/N)? ').upper() == 'Y')
	categoryList(categoryName.replace(' ', '_'), fullPath=fullPath)

if __name__ == '__main__':
	main()
