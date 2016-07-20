import requests
import re

page = requests.get('http://en.wikipedia.org/wiki/Category:Battles_by_country').content.decode('UTF-8')
t = re.findall(r'Battles involving .+</a>', page)
for s in t:
    s = s[18:len(s)-4]
    print(s)