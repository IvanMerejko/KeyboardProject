import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import json
from datetime import datetime

letters_name_array = []
letters_str = 'letters'
current_field_from_json_file = 'duration'
array = []
x = [0.0]


def create_y_labels_name(ax1):
    a_value = ord('a')
    z_value = ord('z')
    constant_for_add = 95
    ax1.set_ylim(a_value-1, z_value+1)
    ax1.set_yticks(np.arange(a_value-1, z_value+1, 1))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
    labels = [item.get_text() for item in ax1.get_yticklabels()]
    for i in range(0, len(labels)):
        if i + constant_for_add in range(ord('a'), ord('z')+1):
            labels[i] = chr(i + constant_for_add)
        else:
            labels[i] = ''
    return labels


def create_x_labels_name(ax1):
    labels = [item.get_text() for item in ax1.get_xticklabels()]
    labels[0] = ''
    for i in range(0, len(letters_name_array)):
        labels[i + 1] = letters_name_array[i]
    return labels


def get_letter_name_from_str(name_str):
    return name_str[1]


def parse_to_seconds(field):
    return datetime.strptime(field, '%H:%M:%S.%f').second


def parse_to_microsecond(field):
    return datetime.strptime(field, '%H:%M:%S.%f').microsecond


with open('log.json') as file:
    data = json.load(file)
    print(data['letters'][0])
    last_character = get_letter_name_from_str(data[letters_str][0]['name'])

    # x.append((parse_to_seconds(data['letters'][0]['pressed']) +
    #           parse_to_microsecond(data['letters'][0]['pressed'])/1000000) * 10)

    array.append((parse_to_seconds(data['letters'][0]['pressed']) +
                 parse_to_microsecond(data['letters'][0]['pressed'])/1000000) * 10)
    array.append((parse_to_seconds(data['letters'][0]['released']) +
                 parse_to_microsecond(data['letters'][0]['released'])/1000000) * 10)

    for letter_info in data['letters'][1::1]:
        letters_name_array.append(last_character)
        last_value = array[len(array) - 1]
        for push_time in range(0, ord(last_character)):
            x.append(last_value)
        last_character = get_letter_name_from_str(letter_info['name'])
        array.append(last_value + (parse_to_seconds(letter_info[current_field_from_json_file]) +
                     parse_to_microsecond(letter_info[current_field_from_json_file]) / 1000000) * 10)

    letters_name_array.append(last_character)

bins = array
hist, bins = np.histogram(x, bins=bins)

width = np.diff(bins)
center = (bins[:-1] + bins[1:]) / 2

fig, ax = plt.subplots()
fig.canvas.draw()

ax.bar(center, hist, align='center', width=width, fill=False, edgecolor='r', linewidth=3)
ax.set_xticks(bins)
ax.set_xticklabels(create_x_labels_name(ax))
ax.set_yticklabels(create_y_labels_name(ax))
ax.grid(which='major',
        color='k')
fig.savefig("out.png")




plt.show()