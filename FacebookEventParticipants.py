# Written by Dmitry Nikolayev (dsnikolaev@gmail.com) in October 2014.
# Protected by The MIT License: http://opensource.org/licenses/MIT

from io import StringIO
from facepy import GraphAPI

def stringify_id_dict(dic):
    sio = StringIO()
    sio.write(dic['name'] + '\n')
    keys = sorted(dic.keys())
    for key in keys:
        if key not in {'name', 'locale', 'updated_time'}:
            sio.write('%s: %s\n' % (key, dic[key]))
    sio.write('\n')
    return sio.getvalue()

graph = GraphAPI('INSERT YOUR ACCESS TOKEN HERE')

facebook_events = [521327744680653, 516658901802881, 632226760224493, 1501124916793597, 289751897886746]

for val in facebook_events:
    name = graph.get(str(val))['name']
    print('Processing %s' % name)
    attendees_iter = graph.get('%d/attending' % val, page = True)
    filename = ''.join([el for el in name if el.isalnum() or el == ' '])
    with open(filename + '.txt', 'w', encoding = 'utf-8') as out:
        for page in attendees_iter:
            for record in page['data']:
                profile = graph.get(str(record['id']))
                out.write(stringify_id_dict(profile))