from pynput import keyboard
from epucklib.epuck_com import EPuckCom
import sys
import time

COM_PORT = ''

wheel_speed = {
    '1': 100,
    '2': 200,
    '3': 300,
    '4': 400,
    '5': 500,
    '6': 600,
    '7': 700,   
    '8': 800,
    '9': 900,
    '0': 1000
}

# Global variables to track robot's movement
move_forward = False # 'w'
move_backward = False # 's'
move_left = False # 'a'
move_right = False # 'd'

current_speed = wheel_speed['5'] # default speed = 500

def get_epuckcomm():
    epuckcomm = EPuckCom(COM_PORT, debug=False)
    
    if (not epuckcomm.connect()):
        print('Cannot connect to robot. Quiting :(')
        return None
        
    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
   
    return epuckcomm
  
# on_press event set the global variable to True if the key is pressed
def on_press(key):
    global move_left, move_right, move_forward, move_backward, current_speed
    try:   
        if key.char in wheel_speed:
            global current_speed
            current_speed = wheel_speed[key.char]
            print(f'Speed set to {current_speed}')

        if key.char == 'w':
            move_forward = True
        elif key.char == 's':
            move_backward = True
        elif key.char == 'a':
            move_left = True
        elif key.char == 'd':
            move_right = True
        # print(f'Key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

# on_release event set the global variable to False if the key is pressed
def on_release(key):
    global move_left, move_right, move_forward, move_backward
    try:
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        
        if key.char == 'w':
            move_forward = False
        elif key.char == 's':
            move_backward = False
        elif key.char == 'a':
            move_left = False
        elif key.char == 'd':
            move_right = False
        # print(f'Key {key.char} released')
    except AttributeError:
        print(f'Special key {key} released')

# This function moves the robot based on the key states
def move_robot(epuckcomm, l_speed_steps_s, r_speed_steps_s):
    # print(f'Left speed: {l_speed_steps_s}, Right speed: {r_speed_steps_s}')
    global move_left, move_right, move_forward, move_backward
    if not epuckcomm:
        return -1 # return -1 indicating error

    # update the left wheel speed and right wheel speed
    if move_forward:
        epuckcomm.state.act_left_motor_speed = l_speed_steps_s
        epuckcomm.state.act_right_motor_speed = r_speed_steps_s
    elif move_backward:
        epuckcomm.state.act_left_motor_speed = -l_speed_steps_s
        epuckcomm.state.act_right_motor_speed = -r_speed_steps_s
    elif move_left:
        epuckcomm.state.act_left_motor_speed = -l_speed_steps_s
        epuckcomm.state.act_right_motor_speed = r_speed_steps_s
    elif move_right:
        epuckcomm.state.act_left_motor_speed = l_speed_steps_s
        epuckcomm.state.act_right_motor_speed = -r_speed_steps_s
    else:
        epuckcomm.state.act_left_motor_speed = 0
        epuckcomm.state.act_right_motor_speed = 0
            
    epuckcomm.send_command() # send the command to the robot

def main():
    try:
        if len(sys.argv) != 2:
            print('Usage: python As1.3.py <COM_PORT>')
            print('Quitting the program')
            return
        
        global COM_PORT, current_speed
        COM_PORT = sys.argv[1]

        print('This will move the robot based on the key press (forward, backward, rotate counter-clockwise, rotate clockwise) for (w, s, a, d) respectively')
        print('Set speed of the robot using the number keys (1-9) from 0 to 1000 (by 100)\n')
        
        # Establish connection with the robot
        epuckcomm = get_epuckcomm()
        print('Giving time for the robot to get the request...')
        time.sleep(0.5) # give time for the robot to get the request
        print('Robot is ready to move...\n')

        # Setting speed of the robot
        print(f'Current speed is {current_speed}\n')

        # Collect events until released
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        print('Moving the robot...\n')
        while True:
            move_robot(epuckcomm, current_speed, current_speed)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print('Quitting the program')
    finally:
        if epuckcomm:
            epuckcomm.stop_all()
            epuckcomm.close()
            print('Connection closed')

if __name__ == '__main__':
    main()
    