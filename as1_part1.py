# import epuck
from epucklib.epuck_com import EPuckCom
from As1lib import *

import time
import random
import os
import sys

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

_debug_as1_1 = False
_script = os.path.basename(__file__)

R_MAX_SPEED = 1200

# epuckcomm      : Epuck robot to perform command
# l_speed_steps_s: speed to set for left motor
# r_speed_steps_s: speed to set for right motor
# l_target_steps : target steps for left motor
# r_target_steps : target steps for right motor
# Hz             : Herts
# 
# retuns         : A tuple containing actual left and right steps moved
def move_steps(epuckcomm, l_speed_steps_s, r_speed_steps_s, 
               l_target_steps, r_target_steps, Hz=10):
    # pre-conditions: The connection with epuckcomm is already established
    if not epuckcomm:
        return () # return empty tuple

# TODO:  
# This function sets the robot’s left and right wheel speed as given, and then starts a control loop that
# monitors the robot odometry readings to see how far (in motor steps) the robot has gone. The loop
# should stop after both the left and right targets were met (note that one may overshoot). Use
# time.sleep() to control the loop speed. After the targets are hit, make the robot stop moving and the
# function return. Return a tuple representing the actual left and right steps moved. Mine is 31 lines.

    left_steps = 0
    right_steps = 0

    # set the last left and right step to what the robot state have
    last_left_steps = epuckcomm.state.sens_left_motor_steps
    last_right_steps = epuckcomm.state.sens_right_motor_steps
    
    # actuators updated
    epuckcomm.state.act_left_motor_speed = l_speed_steps_s
    epuckcomm.state.act_right_motor_speed = r_speed_steps_s
    
    try:
        while (left_steps < l_target_steps) or (right_steps < r_target_steps):
            # debug_print(_debug_as1_1, _script, f'l_left : {last_left_steps}')
            # debug_print(_debug_as1_1, _script, f'l_right: {last_right_steps}')
            # debug_print(_debug_as1_1, _script, '')
            # sending the command    
            # epuckcomm.send_command()
            epuckcomm.data_update()
            
            # update the left_steps and right_steps variables
            
            left_steps += abs(steps_delta(last_left_steps, epuckcomm.state.sens_left_motor_steps))
            right_steps += abs(steps_delta(last_right_steps, epuckcomm.state.sens_right_motor_steps))
            # debug_print(_debug_as1_1, _script, f'a_left : {left_steps}')
            # debug_print(_debug_as1_1, _script, f'a_right: {right_steps}')
            # debug_print(_debug_as1_1, _script, '')
            last_left_steps = epuckcomm.state.sens_left_motor_steps
            last_right_steps = epuckcomm.state.sens_right_motor_steps
            
            time.sleep(1/Hz) # controlling the loop speed
    finally:
        epuckcomm.stop_all()
    
    return (left_steps, right_steps)

def move_straight(epuckcomm, distance_mm, Hz=10):
    
    # pre-conditions: The connection with epuckcomm is already established
    if not epuckcomm:
        return -1 # -1 indicating error
    
    target = mm_to_steps(abs(distance_mm))
    debug_print(_debug_as1_1, _script, f'target: {target}')
    steps_taken = None
    
    if distance_mm < 0:
        steps_taken = move_steps(epuckcomm, -R_MAX_SPEED, -R_MAX_SPEED, target, target, Hz)
    else:
        steps_taken = move_steps(epuckcomm, R_MAX_SPEED, R_MAX_SPEED, target, target, Hz)
    
    l_step_to_mm = steps_to_mm(steps_taken[0])
    r_step_to_mm = steps_to_mm(steps_taken[1])
    
    return (l_step_to_mm + r_step_to_mm) / 2 # return mean of left and right steps

