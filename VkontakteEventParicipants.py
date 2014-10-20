# Written by Dmitry Nikolayev (dsnikolaev@gmail.com) in October 2014.
# Protected by The MIT License: http://opensource.org/licenses/MIT

import urllib.request as ur
import json
from time import sleep
from io import StringIO

def stringify_profile(prof_dic):
    result = StringIO()
    result.write('%s %s\n' % (prof_dic['first_name'], prof_dic['last_name']))
    keys = sorted(prof_dic.keys())
    for key in keys:
        if key == 'uid':
            result.write('Личная страница: https://vk.com/id%d\n' % prof_dic['uid'])
        elif key != 'first_name' and key != 'last_name':
            result.write('%s: %s\n' % (str(key), str(prof_dic[key])))
    result.write('\n')
    return result.getvalue()

event_request_string          = 'https://api.vk.com/method/groups.getMembers?group_id=%s'
event_request_string_w_offset = 'https://api.vk.com/method/groups.getMembers?group_id=%s&offset=%d'
profile_request_string        = 'https://api.vk.com/method/users.get?user_ids=%s&fields=sex,country,bdate,education,universities,occupation'

event_ids = ['77003149', 'marsh_mira_moskva']

for event_id in event_ids:
    print('Processing %s' % event_id)
    with open(event_id + '.txt', 'w', encoding = 'utf-8') as out:
        current_request_string = event_request_string % event_id
        response = ur.urlopen(current_request_string).readall().decode()
        sleep(0.35)
        response_dic = json.loads(response)
        if response_dic['response']['count'] > 1000: # Надо листать.
            participant_count = response_dic['response']['count']
            i = 0
            while i - participant_count < 1000:
                current_request_string = event_request_string_w_offset % (event_id, i)
                page = ur.urlopen(current_request_string).readall().decode()
                sleep(0.35)
                id_list = json.loads(page)['response']['users']
                j = 0
                while j < len(id_list):
                    current_batch = id_list[j:j+300]
                    profiles = ','.join(str(el) for el in current_batch)
                    current_profile_request_string = profile_request_string % profiles
                    profiles_reponse = ur.urlopen(current_profile_request_string).readall().decode()
                    sleep(0.35)
                    profiles_list = json.loads(profiles_reponse)['response']
                    for item in profiles_list:
                        out.write(stringify_profile(item))
                    j += 300
                i += 1000
        else:
            id_list = response_dic['response']['users']
            j = 0
            while j < len(id_list):
                current_batch = id_list[j:j+300]
                profiles = ','.join(str(el) for el in current_batch)
                current_profile_request_string = profile_request_string % profiles
                profiles_reponse = ur.urlopen(current_profile_request_string).readall().decode()
                sleep(0.35)
                profiles_list = json.loads(profiles_reponse)['response']
                for item in profiles_list:
                    out.write(stringify_profile(item))
                j += 300