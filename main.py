from pynput.keyboard import Listener
import datetime


def on_press(key):
    if not hasattr(on_press, '_previous_key'):
        on_press._previous_key = ''
        on_press._is_released = True

    if key != on_press._previous_key or on_press._is_released:
        with open('log.txt', 'a') as f:
            f.write('{0} pressed, time {1}\n'.format(key, datetime.datetime.now().strftime('%H:%M:%S.%f')))
        # print('{0} pressed, time {1}\n'.format(key, datetime.datetime.now().strftime('%H:%M:%S.%f')))
        on_press._previous_key = key
        on_press._is_released = False


def on_release(key):
    on_press._is_released = True
    with open('log.txt', 'a') as f:
        f.write('{0} release, time {1}\n'.format(key, datetime.datetime.now().strftime('%H:%M:%S.%f')))
    # print('{0} release, time {1}\n'.format(key, datetime.datetime.now().strftime('%H:%M:%S.%f')))


with open("log.txt", 'w') as f:
    f.write("")
# Collect events
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

