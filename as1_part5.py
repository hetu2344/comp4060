from As1lib import *
from as1_part1 import move_straight
from epucklib.epuck_com import EPuckCom

import sys

COM_PORT = ''
HZ = 0
SPEED = 100 # mm/s

RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

def get_epuckcomm():
    epuckcomm = EPuckCom(COM_PORT, debug=False)
    
    if not epuckcomm.connect():
        # print()
        print('Cannot connect to robot. Quiting :(')
        print(RED, '**TEST FAILED**', RESET)
        print()
        sys.exit(-1)
        return None
    
    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    return epuckcomm

def perform_test(epuckcomm):
    
    global HZ
    
    for i in range(10):
        input('Press enter to move robot forward 1000mm at 100 mm/s')
        move_straight(epuckcomm, 1000, HZ)
        print('Please put the robot back to origin')

def main():
    
    # python3 as1_part5.py COM_PORT Hz
    if len(sys.argv) != 3:
        print('Please provide COM Port and Frequency of the Loop')
        print('Quiting the program')
        return
    
    global COM_PORT, HZ
    COM_PORT = sys.argv[1]
    HZ = int(sys.argv[2])

    try:    
        epuckcomm = get_epuckcomm()

        perform_test(epuckcomm)
    except KeyboardInterrupt:
        pass
    finally:
        epuckcomm.close()
        
    print('\nEnd of Program...')
    
main()
