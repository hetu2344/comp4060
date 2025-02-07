from epucklib.epuck_com import EPuckCom
from as1_part1 import *
from as1_part4 import *
import sys
import time
import numpy as np

COM_PORT = ''
TRAVEL_DISTANCE_MM = 500 # 0.5m = 500mm
VELOCITY = 300

def get_epuckcomm():
    epuckcomm = EPuckCom(COM_PORT, debug=False)
    
    if (not epuckcomm.connect()):
        print('Cannot connect to robot. Quiting :(')
        return None
        
    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
   
    return epuckcomm

def main():
    try:
        if len(sys.argv) != 2:
            print('Usage: python as1_part3.py <COM_PORT>')
            print('Quitting the program')
            return
        
        global COM_PORT
        COM_PORT = sys.argv[1]

        epuckcomm = get_epuckcomm()
        print('Giving time for the robot to get the request...')
        time.sleep(0.5) # give time for the robot to get the request
        print('Robot is ready to move...\n')

        # Check for connection
        if not epuckcomm:
            return -1
        
        print('Moving the robot forward 0.5m')
        # Move straight 0.5m or 500mm
        distance_moved = move_straight(epuckcomm, TRAVEL_DISTANCE_MM) 
        if not distance_moved or distance_moved == 0:
            return 
        else:
            print(f'Robot moved: {distance_moved}!')
            print('Turning around')

            lsp, rsp, lst, rsp = 0

            left_speed_s, right_speed_s, left_steps, right_steps = diff_drive_inverse_kin(0, VELOCITY / 5, -np.pi/2)
            # Set speed for wheel to turn
            epuckcomm.state.act_left_motor_speed = left_speed_s
            epuckcomm.state.act_right_motor_speed = right_speed_s

            # Set steps for wheel to take for 180 degree turn
            epuckcomm.state.sens_left_motor_steps = left_steps
            epuckcomm.state.sens_right_motor_steps = right_steps

    except KeyboardInterrupt:
            print('Quitting the program')
    finally:
        if epuckcomm:
            epuckcomm.stop_all()
            epuckcomm.close()
        print('Connection closed')

if __name__ == '__main__':
    main()