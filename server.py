from bottle import *
from dateConverters import ct, cf
from databaseWrap import Event, Coord, Country
from get_data import get_data
import json


@route('/favicon.ico')
def get_favicon():
    return static_file('static/favicon.ico', root='/static')

@route('/countries')
# title, url, date_start, date_end, lat, lng, place_comment, comment
def create_response():
    response.set_header('Access-Control-Allow-Origin', '*')
    args_lst = dict(request.query)
    resp = []
    lst = None
    if ('year_from' in args_lst) and ('year_to' in args_lst):
        year_start = ct((int(args_lst['year_from']), 1, 1))
        year_end = ct((int(args_lst['year_to']), 12, 31))
        lst = Country.select().join(Event).where((Country.eventId == Event.id) & (Event.dateStart >= year_start) &
                                                 (Event.dateStart <= year_end))
    else:
        # Country.select().join(Event).where((Country.eventId == Event.id) &
        lst = Country.select()
    for country in lst:
        resp.append(country.name)
    resp = list(set(resp))
    return json.dumps(resp, ensure_ascii=False)

@route('/')
# title, url, date_start, date_end, lat, lng, place_comment, comment
def create_response():
    response.set_header('Access-Control-Allow-Origin', '*')
    args_lst = dict(request.query)
    year_start = None
    year_end = None
    lst = []
    for (key, value) in args_lst.items():
        args_lst[key] = value.strip()
    if 'year' not in args_lst:
        if ('year_to' not in args_lst) or ('year_from' not in args_lst):
            abort(400, 'Bad request, missing some arguments\n I need: year=1234 or \n '\
                    'year_from=1234&year_to=1235')
        else:
            year_start = ct((int(args_lst['year_from']), 1, 1))
            year_end = ct((int(args_lst['year_to']), 12, 31))
    else:
        year_start = ct((int(args_lst['year']), 1, 1))
        year_end = ct((int(args_lst['year']), 12, 31))
    if ('country' not in args_lst) or (args_lst['country'] == ''):
        lst = Event.select().where((Event.dateStart >= year_start) & (Event.dateStart <= year_end))
    else:
        country_names = args_lst['country'].split(',')
        country_bool = Country.name == country_names[0]
        # Country.select().where(Country.eventId == event)
        for i in range(1, len(country_names)):
            country_bool = country_bool | (Country.name == args_lst['country'][i])
        lst = Event.select().join(Country).where(country_bool & (Event.dateStart >= year_start) & (Event.dateStart <= year_end))
    resp = []
    for ev in lst:
        resp.append(get_data(ev.name, ev.url, cf(ev.dateStart), cf(ev.dateEnd), ev.coordId.lat,
                                        ev.coordId.lng, ev.coordId.comment, ev.description))
    return json.dumps(resp, ensure_ascii=False)
    #return str(dict(request.query))


if __name__ == '__main__':
    run(host='0.0.0.0', port=4567, debug=True)