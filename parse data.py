import json
from pathlib import Path
from datetime import datetime

path = Path('log.json')
data = json.loads(path.read_text(encoding='utf-8'))


def get_time_from_string(string):
    return datetime.strptime(string, '%H:%M:%S.%f')


for letter_info in data['letters']:
    duration = get_time_from_string(letter_info['released']) - get_time_from_string(letter_info['pressed'])
    letter_info.setdefault(
        'duration', '{0}'.format(duration)
    )

path.write_text(json.dumps(data), encoding='utf-8')