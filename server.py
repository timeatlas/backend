from bottle import *
from dateConverters import ct, cf
from databaseWrap import Event, Coord, Country
from get_data import get_data, get_coord_data, get_info
import json

# Set header which allows CORS. It doesn't apply header to error page (at least to 500 error; don't know why)
@hook('after_request')
def enable_cors():
    response.set_header('Access-Control-Allow-Origin', '*')

@route('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='./static')

@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./static')

@error(404)
def error404(error):
    return static_file('404.html', root='./static')

@error(500)
def error500(error):
    response.set_header('Access-Control-Allow-Origin', '*')

@error(403)
def error403(error):
    return static_file('403.html', root='./static')

@route('/countries')
# title, url, date_start, date_end, lat, lng, place_comment, comment
def create_response():
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

    print('Query:', lst, file = sys.stderr)

    for country in lst:
        resp.append(country.name)
    result = {}
    for el in resp:
        if not el in result:
            result[el] = 0
        result[el] += 1
    result = result.items()
    t = []
    for tup in result:
        t.append((tup[1], tup[0]))
    result = list(reversed(sorted(t)))
    if 'counter' not in args_lst:
        resp = []
        for el in result:
            resp.append(el[1])
    else:
        resp = result
    return json.dumps(resp, ensure_ascii=False)


@route('/by_coord')
def desc_by_coord():
    args_lst = dict(request.query)
    if ('lat' not in args_lst) or ('lng' not in args_lst):
        return static_file('403.html', root='./static')

    resp = []
    lst = Event.select().join(Coord).where((Event.coordId == Coord.id) & (Coord.lat == args_lst['lat']) & (Coord.lng == args_lst['lng']))

    print('Query:', lst, file = sys.stderr)

    for ev in lst:
        resp.append(get_info(ev.id, ev.name, ev.url, cf(ev.dateStart), cf(ev.dateEnd), ev.description))
    return json.dumps(resp, ensure_ascii=False)


@route('/by_id')
def desc_by_coord():
    args_lst = dict(request.query)
    if 'id' not in args_lst:
        return static_file('403.html', root='./static')

    resp = []
    id_lst = args_lst['id'].split(',')
    lst = Event.select().where(Event.id << id_lst)

    print('Query:', lst, file = sys.stderr)

    for ev in lst:
        resp.append(get_info(ev.id, ev.name, ev.url, cf(ev.dateStart), cf(ev.dateEnd), ev.description))
    return json.dumps(resp, ensure_ascii=False)


@route('/')
# title, url, date_start, date_end, lat, lng, place_comment, comment
def create_response():
    args_lst = dict(request.query)
    year_start = None
    year_end = None
    lst = []
    for (key, value) in args_lst.items():
        args_lst[key] = value.strip()
    if 'year' not in args_lst:
        if ('year_to' not in args_lst) or ('year_from' not in args_lst):
            return static_file('403.html', root='./static')
            # abort(400, 'Bad request, missing some arguments\n I need: year=1234 or \n '\
            #        'year_from=1234&year_to=1235')
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

    print('Query:', lst, file = sys.stderr)

    if 'only_coord' in args_lst:
        for ev in lst:
            resp.append(get_coord_data(ev.id, ev.coordId.lat,
                                        ev.coordId.lng, ev.coordId.comment))
    else:
        for ev in lst:
            resp.append(get_data(ev.id, ev.name, ev.url, cf(ev.dateStart), cf(ev.dateEnd), ev.coordId.lat,
                                            ev.coordId.lng, ev.coordId.comment, ev.description))
    return json.dumps(resp, ensure_ascii=False)
    #return str(dict(request.query))


if __name__ == '__main__':
    run(host='0.0.0.0', port=4567, debug=True)
