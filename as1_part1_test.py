from as1_part1 import *

def main():        
    epuckcomm = EPuckCom("/dev/cu.usbmodem3011", debug=False)
    
    if not epuckcomm.connect():
        print("Could not connect to the robot, quitting :(")
        return
    
    epuckcomm.enable_sensors = True
    epuckcomm.send_command()
    time.sleep(0.5)
    
    # print(move_steps(epuckcomm, R_MAX_SPEED, R_MAX_SPEED, 1000, 1000))
    # print(move_steps(epuckcomm, -R_MAX_SPEED, -R_MAX_SPEED, 1000, 1000))
    # print(move_straight(epuckcomm, 130))
    # print(move_straight(epuckcomm, -130))
    
    # print(move_steps(epuckcomm, R_MAX_SPEED, -R_MAX_SPEED, 1290, 1290))
    print(move_steps(epuckcomm, 0, R_MAX_SPEED, 0, 2580))
    
    epuckcomm.close()
    
    return
    
main()