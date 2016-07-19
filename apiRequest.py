import hashlib
import urllib.request
import os.path


BASE_URL = 'https://en.wikipedia.org/w/api.php?'


def cachingAPIRequest(params):
    filename = hashlib.sha512(params.encode('utf-8')).hexdigest()
    if os.path.isfile(os.path.join('apiCache', filename)):
        with open(os.path.join('apiCache', filename), encoding='utf-8') as f:
            return f.read()
    else:
        try:
            res = urllib.request.urlopen(BASE_URL + params).read().decode('utf-8')
        except:
            return ''
        with open(os.path.join('apiCache', filename), 'w', encoding='utf-8') as f:
            f.write(res)
        return res
