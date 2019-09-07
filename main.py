from pynput.keyboard import Key, Listener
import datetime



def on_press(key):

    if not hasattr(on_press, '_previous_key'):
        on_press._previous_key = ''
        on_press._is_released = True


    if(key != on_press._previous_key or on_press._is_released ):
        print('{0} pressed, time{1}'.format(key, datetime.datetime.now()))
        on_press._previous_key = key
        on_press._is_released = False


def on_release(key):
    on_press._is_released = True
    print('{0} release, time{1}'.format(key, datetime.datetime.now()))

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()




