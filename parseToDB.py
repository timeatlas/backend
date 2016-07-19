from contextlib import redirect_stdout
import categoryLister
from parse_what_i_know import get_coord
import parse_what_i_know
import io
import wikilib
from dateConverters import ct, cf
import databaseWrap
from databaseWrap import Event, Coord
import datetime
from apiRequest import cachingAPIRequest
import urllib.parse
import json

URL_BASE = 'https://en.wikipedia.org/wiki/'

def main():
    databaseWrap.createTables()
    categoryLister.main()
    pagesListIO = io.StringIO()
    with redirect_stdout(pagesListIO):
        parse_what_i_know.main()
    pagesList = pagesListIO.getvalue().split('\n')
    for name in pagesList:
        if name.strip() == '':
            continue
        print('<<{}>>'.format(name))
        page = categoryLister.cachingGetPage(name)
        url = URL_BASE + name.replace(' ', '_')
        # coordLat, coordLng = map(float, get_coord(page).decode().split())
        coordsAns = cachingAPIRequest(urllib.parse.urlencode({'action': 'query', 'prop': 'coordinates', 'titles': name, 'format': 'json'}))
        coordsAns = json.loads(coordsAns)
        try:
            coordLat = list(coordsAns['query']['pages'].values())[0]['coordinates'][0]['lat']
            coordLng = list(coordsAns['query']['pages'].values())[0]['coordinates'][0]['lon']
        except Exception as e:
            continue
        if 'dim' in list(coordsAns['query']['pages'].values())[0]['coordinates'][0]:
            coordRad = list(coordsAns['query']['pages'].values())[0]['coordinates'][0]['dim']
        infoboxData = wikilib.parse_infobox_military_conflict(wikilib.get_infobox(page)[0])
        if 'place' in infoboxData:
            coordComment = infoboxData['place']
        else:
            coordComment = ''
        partOf = None
        print(infoboxData['date'])
        try:
            dateStart, dateEnd = map(lambda d: ct(list(reversed(d))), infoboxData['date'])
        except Exception as e:
            print(e)
            dateStart = datetime.date(1, 1, 1)
            dateEnd = datetime.date(1, 1, 1)
        coord = Coord.create(lat=coordLat, lng=coordLng, comment=coordComment, radius=0.)
        description = categoryLister.cachingGetSummary(name)
        Event.create(name=name, url=url, coordId=coord, dateStart=dateStart, dateEnd=dateEnd, description=description) 

if __name__ == '__main__':
    main()
