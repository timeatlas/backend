from bottle import *

@route('/')
def root():
    return "<p> hyak hyak i v production </p>"


if __name__ == '__main__':
    run(host='localhost', port=4567, debug=True)