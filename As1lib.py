import math

# TODO:
#   Date 21 Jan 2025
#       - Define constants instead of hard-coded values                         : Done by Het on 21 Jan
#       - Measure the wheel diameter and wheel based and update it              :
#       - Research for how many bit the stepper motor uses for counting steps   :

# CONSTANTS
COUNTER_BITS = 32 # No. of bits used by stepper motor to store counter
WHEEL_DIAMETER = 41 # in mm
STEPS_PER_REVOLUTION = 1000

# steps_delta(last, current): int, calculates the difference in robot steps from the last
# position to the current, accounting for counter wraparound, and returns it as a signed integer.
# This one is tricky. Mine is 5 lines including def and return.
def steps_delta(last, current):
    # Step 1: Compute raw difference with wraparound
    delta = (current - last) % (2**COUNTER_BITS)  # Ensures diff is within [0, 2^32 - 1]

    # Step 2: Interpret as signed integer
    if delta >= 2**(COUNTER_BITS - 1):
        delta -= 2**COUNTER_BITS  # Convert to negative value
    
    return delta
    

# steps_to_rad(steps): float, converts signed motor steps to signed radians, and returns that
# value, using your knowledge of the motor construction. 2 lines
def steps_to_rad(steps):
    # (steps * 360 / 1000): Degree moved (1 revolution of moter have 1000 steps)
    # Then multiplying degree moved with (math.pi / 180) to get radians
    return float((steps * 360 / STEPS_PER_REVOLUTION) * (math.pi / 180))

# rad_to_steps(rad): float, converts signed radians to signed motor steps, and returns that
# value, using your knowledge of the motor construction. 2 lines
def rad_to_steps(rad):
    # rad * 180 / math.pi: Converting rad to degree
    # from degree figuring out # of steps by multiplying it by (1000 / 360)
    return float((rad * 180 / math.pi) * (STEPS_PER_REVOLUTION / 360))

# rad_to_mm(rad): float, converts the given signed radians of wheel rotation into expected
# signed ground distance, and returns that value. 2 lines
def rad_to_mm(rad):
    # Diameter of wheel is 41 mm
    # rad * 41 / 2: distance travelled in mm
    return float(rad * WHEEL_DIAMETER / 2)

# mm_to_rad(mm): float, converts the given mm distance into expected radians of wheel
# rotation, and returns that value. 2 lines
def mm_to_rad(mm):
    return float(mm * 2 / WHEEL_DIAMETER)

# steps_to_mm(steps): float, converts motor steps into expected ground distance, and returns
# that value. 2 lines
def steps_to_mm(steps):
    return float(steps * math.pi * WHEEL_DIAMETER / STEPS_PER_REVOLUTION)

# mm_to_steps(mm): float, converts expected ground distance into motor steps, and returns
# that value. 2 lines
def mm_to_steps(mm):
    return float(mm * STEPS_PER_REVOLUTION / math.pi / WHEEL_DIAMETER)

# print_pose ( (x_mm, y_mm, theta_rad) ), prints x,y,theta while converting theta to
# degrees. 3 lines
def print_pose(pos):
    # print(f'({pos[0]}mm, {pos[1]}mm, {pos[2] * 180 / math.pi}°)')
    # If for any reason the print_pose gives error then
    # uncomment the bottom line and comment the above line
    print(f'({round(pos[0])}, {round(pos[1])}, {round((pos[2] * 180 / math.pi) % 360)})')
    
def ret_pose(pos):
    # print(f'({pos[0]}mm, {pos[1]}mm, {pos[2] * 180 / math.pi}°)')
    # If for any reason the print_pose gives error then
    # uncomment the bottom line and comment the above line
    return (pos[0], pos[1], pos[2] * 180 / math.pi)
    
# print_pose((7, 7, math.pi))

def debug_print(_print, script, msg):
    if(_print): print(script+": "+msg)