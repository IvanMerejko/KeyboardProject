import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
import numpy as np
import json
from datetime import datetime
import os
user_name = "diana"


letters_name_array = []
letters_str = 'letters'
current_field_from_json_file = 'duration'
labels_name_array = []
array = []
x = [0.0]
special_constant = {
    'Key.space': ord('z') + 1,
    'Key.shift': ord('z') + 2,
    'Key.backspace': ord('z') + 3,
    'Key.tab': ord('z') + 4,
    'Key.caps_lock': ord('z') + 5,
    'Key.shift_r': ord('z') + 6,
    'Key.shift_l': ord('z') + 7,
    'Key.enter': ord('z') + 8
}

Space_constant = ord('z') + 1
print(Space_constant)
def create_labels_name(ax1):
    rects = ax1.patches

    for rect, label in zip(rects, labels_name_array):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')


def append_n_times(append_to, value, time_number):
    for i in range(0, time_number):
        append_to.append(value)


def create_y_labels_name(ax1):
    a_value = ord('a')
    z_value = ord('z')
    constant_for_add = 95
    ax1.set_ylim(a_value-1, z_value+1)
    ax1.set_yticks(np.arange(a_value-1, z_value+2, 1))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))
    labels = [item.get_text() for item in ax1.get_yticklabels()]
    for i in range(0, len(labels)):
        if i + constant_for_add in range(ord('a'), ord('z')+2):
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
    print("get_letter_name_from_str = ", name_str)
    if name_str in special_constant.keys():
        return name_str
    return name_str[1]


def parse_to_seconds(field):
    return datetime.strptime(field, '%H:%M:%S.%f').second


def parse_to_microseconds(field):
    return datetime.strptime(field, '%H:%M:%S.%f').microsecond

def parse_one_file(file_name, file_number):
    print(file_name)
    with open(file_name) as file:
        data = json.load(file)
        first_letter = data['letters'][0]
        last_character = get_letter_name_from_str(first_letter['name'])

        first_letter_time = (parse_to_seconds(first_letter['pressed']) +
                             parse_to_microseconds(first_letter['pressed'])/1000000) * 10
        number_for_first = ord(last_character) if len(last_character) == 1 else special_constant[last_character]
        append_n_times(x, first_letter_time, number_for_first)

        array.append((parse_to_seconds(first_letter['pressed']) +
                     parse_to_microseconds(first_letter['pressed'])/1000000) * 10)
        array.append((parse_to_seconds(first_letter['released']) +
                     parse_to_microseconds(first_letter['released'])/1000000) * 10)

        if current_field_from_json_file == 'time_after_last_press':
            labels_name_array.append(0)
        else:
            second = parse_to_seconds(first_letter[current_field_from_json_file])
            microsecond = parse_to_microseconds(first_letter[current_field_from_json_file])
            labels_name_array.append(second + microsecond / 1000000)

        for letter_info in data['letters'][1::1]:
            print(letter_info)
            letters_name_array.append(last_character)
            last_value = array[len(array) - 1]
            print(last_character)
            number = ord(last_character) if len(last_character) == 1 else special_constant[last_character]
            print(number)
            append_n_times(x, last_value, number)
            last_character = get_letter_name_from_str(letter_info['name'])
            seconds = parse_to_seconds(letter_info[current_field_from_json_file])
            microseconds = parse_to_microseconds(letter_info[current_field_from_json_file])
            labels_name_array.append(seconds + microseconds/1000000)
            array.append(last_value + (seconds + microseconds/1000000) * 10)

        letters_name_array.append(last_character)
    print(x)
    bins = array
    hist, bins = np.histogram(x, bins=bins)
    width = np.diff(bins)
    center = (bins[:-1] + bins[1:]) / 2
    margins = {
        "left"   : 0.040,
        "bottom" : 0.060,
        "right"  : 0.990,
        "top"    : 0.990
    }
    figure = Figure(facecolor="None")
    figure.subplots_adjust(**margins)
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 15)
    ax.axis('off')
    fig.canvas.draw()
    ax.bar(center, hist, width=width)
    ax.set_xticks(bins)
    ax.set_xticklabels(create_x_labels_name(ax))
    ax.set_yticklabels(create_y_labels_name(ax))
    fig.savefig("test/{name}.{number}.png".format(name=user_name,
                                                  number=file_number), dpi=5)
    array.clear()
    letters_name_array.clear()
    labels_name_array.clear()
    x.clear()
    x.append(0.0)
    plt.show()


number = 1
dir_path = "{name}".format(name=user_name)
for file in os.listdir(dir_path):
    parse_one_file(dir_path+'/'+file, number)
    number += 1
