import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime


letters_str = 'letters'
current_field_from_json_file = 'duration'
array = []
x = [0.0]

with open('log.json') as file:
    data = json.load(file)
    print(data['letters'][0])
    last_character = data[letters_str][0]['name']
    x.append((datetime.strptime(data[letters_str][0]['pressed'], '%H:%M:%S.%f').second +
                  datetime.strptime(data['letters'][0]['pressed'], '%H:%M:%S.%f').microsecond / 1000000) * 10 )
    x.append((datetime.strptime(data['letters'][0]['pressed'], '%H:%M:%S.%f').second +
              datetime.strptime(data['letters'][0]['pressed'], '%H:%M:%S.%f').microsecond / 1000000) * 10)
    array.append((datetime.strptime(data['letters'][0]['pressed'], '%H:%M:%S.%f').second +
                  datetime.strptime(data['letters'][0]['pressed'], '%H:%M:%S.%f').microsecond / 1000000) * 10 )
    array.append((datetime.strptime(data['letters'][0]['released'], '%H:%M:%S.%f').second +
                  datetime.strptime(data['letters'][0]['released'], '%H:%M:%S.%f').microsecond / 1000000) * 10)

    for i in data['letters'][1::1]:
        print(i)
        last_value = array[len(array) - 1]
        print(ord(last_character[1]))
        for push_time in range(0, ord(last_character[1])):
            x.append(last_value)
        last_character = i['name']
        array.append(last_value + (datetime.strptime(i[current_field_from_json_file], '%H:%M:%S.%f').second +
                      datetime.strptime(i[current_field_from_json_file], '%H:%M:%S.%f').microsecond / 1000000) * 10)

    for push_time in range(0, ord(last_character[1])):
        x.append(last_value)

print(x)
print(array)


bins = array
# bins = [0, 40, 60, 75, 90, 110, 125, 140, 160, 180]
hist, bins = np.histogram(x, bins=bins)

width = np.diff(bins)
center = (bins[:-1] + bins[1:]) / 2

fig, ax = plt.subplots()
ax.bar(center, hist, align='center', width=width)
ax.set_xticks(bins)

fig.savefig("out.png")

plt.show()