from as1_part1 import *

RED = '\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

COM_PORT = ''

total_test = 6
test_pass = 0

def print_stats():
    print()
    print('Total Tests       : ', YELLOW, total_test, RESET)
    print('Total Tests Passed: ', GREEN, test_pass, RESET)
    print('Total Tests Failed: ', RED, total_test - test_pass, RESET)
    print()

def print_test_fail():
    # print()
    print(RED, '**TEST FAILED**', RESET)
    print()
    
def print_test_pass():
    # print()
    print(GREEN, '**TEST PASSED**', RESET)
    print()
    global test_pass
    test_pass += 1

def get_epuckcomm():
    epuckcomm = EPuckCom(COM_PORT, debug=False)
    
    if not epuckcomm.connect():
        # print()
        print('Cannot connect to robot. Quiting :(')
        print(RED, '**TEST FAILED**', RESET)
        print()
        return None
    
    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    return epuckcomm

def test_move_step_fwd():
    print('Running Test No. 1')
    print('Moving Robot forward by 1000 steps')
    epuckcomm = get_epuckcomm()
    
    if not epuckcomm:
        return

    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    steps_moved = move_steps(epuckcomm, R_MAX_SPEED, R_MAX_SPEED, 1000, 1000)
    
    if not steps_moved or len(steps_moved) == 0:
        print_test_fail()
    else:
        print('Target steps: (1000, 1000)')
        print('Steps moved :', steps_moved)
        print_test_pass()
    
    epuckcomm.close()
    
        
def test_move_step_bck():
    print('Running Test No. 2')
    print('Moving Robot backward by 1000 steps')
    epuckcomm = get_epuckcomm()
    
    if not epuckcomm:
        return

    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    steps_moved = move_steps(epuckcomm, -R_MAX_SPEED, -R_MAX_SPEED, 1000, 1000)
    
    if not steps_moved or len(steps_moved) == 0:
        print_test_fail()
    else:
        print('Target steps: (1000, 1000)')
        print('Steps moved :', steps_moved)
        print_test_pass()
    
    epuckcomm.close()
        
def test_move_step_clock():
    print('Running Test No. 3')
    print('Moving Robot, on spot, clockwise by 1 rotation')
    epuckcomm = get_epuckcomm()
    
    if not epuckcomm:
        return

    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    steps_moved = move_steps(epuckcomm, R_MAX_SPEED, -R_MAX_SPEED, 1290, 1290)
    
    if not steps_moved or len(steps_moved) == 0:
        print_test_fail()
    else:
        print('Target steps: (1290, 1290)')
        print('Steps moved :', steps_moved)
        print_test_pass()
    
    epuckcomm.close()
    
def test_move_step_pivot():
    print('Running Test No. 4')
    print('Turning Robot to right by 1 rotation')
    epuckcomm = get_epuckcomm()
    
    if not epuckcomm:
        return

    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    steps_moved = move_steps(epuckcomm, R_MAX_SPEED, 0, 2580, 0)
    
    if not steps_moved or len(steps_moved) == 0:
        print_test_fail()
    else:
        print('Target steps: (2580, 0)')
        print('Steps moved :', steps_moved)
        print_test_pass()
    
    epuckcomm.close()
    
def test_move_straight_fwd():
    print('Running Test No. 5')
    print('Moving Robot straight forward by 14 cm(s)')
    epuckcomm = get_epuckcomm()
    
    if not epuckcomm:
        return

    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    distance_moved = move_straight(epuckcomm, 140)
    
    if not distance_moved or distance_moved == 0:
        print_test_fail()
    else:
        print('Target distance: 140 cm(s)')
        print('Distance moved :', distance_moved, 'cm(s)')
        print_test_pass()
    
    epuckcomm.close()
    
def test_move_straight_bck():
    print('Running Test No. 6')
    print('Moving Robot straight backward by 14 cm(s)')
    epuckcomm = get_epuckcomm()
    
    if not epuckcomm:
        return

    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    
    distance_moved = move_straight(epuckcomm, -140)
    
    if not distance_moved or distance_moved == 0:
        print_test_fail()
    else:
        print('Target distance: 140 cm(s)')
        print('Distance moved :', distance_moved, 'cm(s)')
        print_test_pass()
    
    epuckcomm.close()

def main():
    
    if len(sys.argv) != 2:
        print('Please provide COM Port')
        print('Quiting the program')
        return
    
    global COM_PORT
    COM_PORT = sys.argv[1]
    
    
    print('This will run 6 different test related to part 1 of assignment 1')
    
    # First test
    test_move_step_fwd()
    # Second test
    test_move_step_bck()
    # Third test
    test_move_step_clock()
    # Fourth test
    test_move_step_pivot()
    # Fifth test
    test_move_straight_fwd()
    # Sixth test
    test_move_straight_bck()
    
    print_stats()
    return
    
main()