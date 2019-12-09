import json
from pathlib import Path
from datetime import datetime

path = Path('log.json')
data = json.loads(path.read_text(encoding='utf-8'))

previouse_button_pressed_time = None

def get_time_from_string(string):
    return datetime.strptime(string, '%H:%M:%S.%f')


for letter_info in data['letters']:
    released_time = get_time_from_string(letter_info['released'])
    pressed_time = get_time_from_string(letter_info['pressed'])
    time_between_pressed = None
    if not previouse_button_pressed_time:
        previouse_button_pressed_time = pressed_time
    else:
        time_between_pressed = pressed_time - previouse_button_pressed_time
        previouse_button_pressed_time = pressed_time


    duration = released_time - pressed_time
    letter_info.setdefault(
        'duration', '{0}'.format(duration)
    )
    letter_info.setdefault(
        'time_after_last_press', '{0}'.format(time_between_pressed)
    )

path.write_text(json.dumps(data), encoding='utf-8')