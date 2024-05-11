from pyjoystick.sdl2 import run_event_loop
import yaml
import rpyc

with open('joystick_config.yaml', 'r') as file:
    prime_service = yaml.safe_load(file)

conn = rpyc.connect("localhost", 18861)

def print_add(joy):
    print('Added', joy)

def print_remove(joy):
    print('Removed', joy)

def key_received(key):
    # print('received', key, type(key), dir(key))
    try:
        key_name = prime_service['joystick'][key.keyname]
    except:
        key_name = key.keyname
    print(key_name, key.get_value())
    conn.root.setJoystickStatus(key_name, key.get_value())
    if key.get_value() < 0.1:
        conn.root.setJoystickStatus(key_name, key.get_value())
    

run_event_loop(print_add, print_remove, key_received)