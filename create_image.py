from PIL import Image, ImageDraw
import json
from datetime import datetime
import os
user_name = "diana"
duration_filed = 'duration'
last_pressed_time_field = 'time_after_last_press'
symbols_number = 40
matrix = dict()
def parse_to_seconds(field):
    return datetime.strptime(field, '%H:%M:%S.%f').second


def parse_to_microseconds(field):
    return datetime.strptime(field, '%H:%M:%S.%f').microsecond

def get_letter_int(letter):
    return ord(letter) - ord('a')

def get_color(second, microsecond):
    constant = 1000000
    return (second * constant + microsecond) / constant

def get_duration(letter_info):
    second = parse_to_seconds(letter_info[duration_filed])
    microsecond = parse_to_microseconds(letter_info[duration_filed])
    return get_color(second, microsecond)

def get_time_after_last_pressed(letter_info):
    second = parse_to_seconds(letter_info[last_pressed_time_field])
    microsecond = parse_to_microseconds(letter_info[last_pressed_time_field])
    return get_color(second, microsecond)

def get_symbol_color(letter_info):
    if len(letter_info['name']) == 3:
        return get_letter_int(letter_info['name'][1]) / symbols_number

def get_line_number(name):
    if len(name) == 3:
        return ord(name[1]) - ord('a')

def scale(value):
    return (int)(value * 255)

def create_image():
    image = Image.new('RGB', (40, 40))
    draw  = ImageDraw.Draw(image)
    print(matrix)
    for point in matrix.keys():

        x, y = point
        r, g, b= matrix[point]
        for i in range(y, 40):
            draw.point((x, i), (scale(r), scale(g), scale(b)))

        draw.point((x, y), (scale(r), scale(g), scale(b)))
    image.save('try1.png')


def parse_one_file(file_name, file_number):
    current_column = 1
    matrix.clear()

    with open(file_name) as file:
        data = json.load(file)
        first_letter = data['letters'][0]
        print(get_letter_int(first_letter['name'][1]))
        for letter_info in data['letters'][1::1]:
            matrix[(current_column, get_line_number(letter_info['name']))] = \
            {
                get_symbol_color(letter_info),
                get_duration(letter_info),
                get_time_after_last_pressed(letter_info)
            }
            current_column += 1


number = 1
dir_path = "{name}".format(name=user_name)
for file in os.listdir(dir_path):
    parse_one_file('diana.843670.json', number)
    create_image()
    number += 1

print(matrix)