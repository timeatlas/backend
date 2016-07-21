from contextlib import redirect_stdout
import categoryLister
from parse_what_i_know import get_coord
import parse_what_i_know
import io
import wikilib
from dateConverters import ct, cf
import databaseWrap
from databaseWrap import Event, Coord, Country
import datetime
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
            print('WTF, empty name?')
            continue
        print('<<{}>>'.format(name))
        page = categoryLister.cachingGetPage(name)
        url = URL_BASE + name.replace(' ', '_')
        # coordLat, coordLng = map(float, get_coord(page).decode().split())
        coords = wikilib.get_page_coord(name)
        if len(coords) == 3:
            coordLat, coordLng, coordRad = coords
        else:
            coordLat, coordLng = coords
            coordRad = 0.
        infoboxData = wikilib.parse_infobox_military_conflict(wikilib.get_infobox(page))
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
        event = Event.create(name=name, url=url, coordId=coord, dateStart=dateStart, dateEnd=dateEnd, description=description) 
        if 'combatants' in infoboxData:
            for combatant in infoboxData['combatants']:
                Country.create(name=combatant, eventId=event)

if __name__ == '__main__':
    main()
