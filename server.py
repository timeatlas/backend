from bottle import *

@route('/')
def root():
    return str(dict(request.query))


if __name__ == '__main__':
    run(host='localhost', port=4567, debug=True)