import urllib.request
import urllib.parse
import json

BASE = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmlimit=500&format=json'

def pagesList(categoryName, cmtype='page'):
	req = BASE + '&' + urllib.parse.urlencode({'cmtitle': categoryName, 'cmtype': cmtype})
	res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
	members = res['query']['categorymembers']
	while 'continue' in res:
		cReq = req + '&cmcontinue=' + res['continue']['cmcontinue']
		res = json.loads(urllib.request.urlopen(cReq).read().decode('utf-8'))
		members += res['query']['categorymembers']
	return members

def recursivePagesList(categoryName, lim=-1):
	if lim == 0:
		return []
	members = pagesList(categoryName)
	for cat in pagesList(categoryName, cmtype='subcat'):
		title = cat['title'].replace(' ', '_')
		members += recursivePagesList(title, lim=lim - 1)
	return members

