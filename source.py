from pynput.keyboard import Listener
import datetime

import json
from pathlib import Path

start_time = datetime.datetime.now()

start_json = {}
start_json["letters"] = []
with open('log.json', 'w') as file:
    json.dump(start_json, file)



def write_to_json(key, action, time, is_released = False):
    path = Path('log.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    if not is_released:
        data['letters'].append({
            'name': '{0}'.format(key),
            '{0}'.format(action): '{0}'.format(time)
        })
        path.write_text(json.dumps(data), encoding='utf-8')
    else:
        data['letters'][-1].setdefault(
            '{0}'.format(action), '{0}'.format(time)
        )
        path.write_text(json.dumps(data), encoding='utf-8')


def on_press(key):
    if not hasattr(on_press, '_previous_key'):
        on_press._previous_key = ''
        on_press._is_released = True


    if key != on_press._previous_key or on_press._is_released:
        with open('log.txt', 'a') as f:
            f.write('{0} pressed, time {1}\n'.format(key, datetime.datetime.now() - start_time))
        # print('{0} pressed, time {1}\n'.format(key, datetime.datetime.now().strftime('%H:%M:%S.%f')))
        on_press._previous_pressed_symbol = ''

    if key != on_press._previous_key or on_press._is_released:
        write_to_json('{0}'.format(key),
                      'pressed',
                      '{0}'.format(datetime.datetime.now()- start_time))

        on_press._previous_pressed_symbol = key
        on_press._previous_key = key
        on_press._is_released = False


def on_release(key):
    on_press._is_released = True
    write_to_json('{0}'.format(key),
                    'released',
                    '{0}'.format(datetime.datetime.now() - start_time),
                    True)


# Collect events
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

