import json
import random
import pprint

def get_random_period():
    year = random.randint(1000, 2000)
    return {
        'from_date': {
            'year': year,
            'month': random.randint(1, 12),
            'day': random.randint(1, 28),
            'comment': ''
        },
        'to_date': {
            'year': year + random.randint(1, 100),
            'month': random.randint(1, 12),
            'day': random.randint(1, 28),
            'comment': ''
        }
    }

def get_random_data():
    data = {}
    number = str(random.randint(1, 1000000))
    data['coord'] = {'lat': random.uniform(10, 80), 'lng': random.uniform(10, 80),
                     'comment': 'random place № '+number}
    data['period'] = get_random_period()
    data['title'] = 'random battle № '+number
    data['comment'] = 'Mega Battle with Mane Six and Evil № '+number
    data['url'] = 'wikipedia.org/wiki/'+data['comment']
    data['type'] = 'Battle'
    data['data'] = {
        'sides': ['Mane 6', 'Evil'],
        'winners': ['Mane Six'],
        'result': 'Mane Six Wins!'
    }
    return data

def pack(data, file):
    print(data)
    f = open(file, 'w', encoding='UTF-8')
    print(data, file=f)
    f.close()

if __name__ == '__main__':
    for i in range(10):
        pack(json.dumps(get_random_data(), ensure_ascii=False), 'test_'+str(i)+'.json')