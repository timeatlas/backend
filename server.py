from bottle import *
from dateConverters import ct, cf
from databaseWrap import Event, Coord
from get_data import get_data
import json

@route('/')
# title, url, date_start, date_end, lat, lng, place_comment, comment
def create_response():
    args_lst = dict(request.query)
    year_start = None
    year_end = None
    lst = []
    if 'year' not in args_lst:
        if ('year_to' not in args_lst) or ('year_from' not in args_lst):
            abort(400, 'Bad request, missing some arguments\n I need: year=1234&type=military_conflict or \n '\
                    'year_from=1234&year_to=1235')
        else:
            year_start = ct((int(args_lst['year_from']), 1, 1))
            year_end = ct((int(args_lst['year_to']), 12, 31))
    else:
        year_start = ct((int(args_lst['year']), 1, 1))
        year_end = ct((int(args_lst['year']), 12, 31))

    lst = Event.select().where((Event.dateStart >= year_start) & (Event.dateStart <= year_end))
    resp = []
    for ev in lst:
        resp.append(json.dumps(get_data(ev.name, ev.url, cf(ev.dateStart), cf(ev.dateEnd), ev.coordId.lat,
                                        ev.coordId.lng, ev.coordId.comment, ev.description), ensure_ascii=False))
    return str(resp)
    #return str(dict(request.query))


if __name__ == '__main__':
    run(host='0.0.0.0', port=4567, debug=True)