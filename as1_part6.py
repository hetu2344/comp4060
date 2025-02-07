from epucklib.epuck_com import EPuckCom
from as1_part1 import *
from as1_part4 import *
import sys
import time
import numpy as np

COM_PORT = ''
TRAVEL_DISTANCE_MM = 500 # 0.5m = 500mm
WHEEL_SPEED = 500

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

        # Check for connection
        if not epuckcomm:
            return
        
        print('Giving time for the robot to get the request...')
        time.sleep(0.5) # give time for the robot to get the request
        print('Robot is ready to move...\n')

        print('Moving the robot forward 0.5m')
        # Move straight 0.5m or 500mm
        distance_moved = move_straight(epuckcomm, TRAVEL_DISTANCE_MM) 
        if not distance_moved or distance_moved == 0:
            return 
        else:
            print(f'Robot moved: {distance_moved}!')
            print('Turning around')
            time.sleep(0.1)
            left_steps, right_steps = move_steps(epuckcomm, *diff_drive_inverse_kin(0, WHEEL_SPEED, -np.pi), Hz=30) # Tune Hz for correct angle or else it would not turn 180 degree
            print(left_steps, right_steps)

            print('Moving back to original location')
            time.sleep(0.1)
            distance_moved = move_straight(epuckcomm, TRAVEL_DISTANCE_MM)
            print(f'Robot moved: {distance_moved}!')
            if not distance_moved or distance_moved == 0:
                return  
            print('Done!')
            
    except KeyboardInterrupt:
            print('Quitting the program')
    finally:
        if epuckcomm:
            epuckcomm.stop_all()
            epuckcomm.close()
        print('Connection closed')

if __name__ == '__main__':
    main()