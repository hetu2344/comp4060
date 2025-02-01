from epucklib.epuck_com import EPuckCom
from As1lib import *
import numpy as np

WHEEL_BASE_MM = 53

def cal_R(left_speed, right_speed):
    return ( WHEEL_BASE_MM / 2) * ( ( left_speed + right_speed ) / ( right_speed - left_speed ))

def diff_drive_inverse_kin(distance_mm, speed_mm_s, omega_rad):
    if distance_mm == 0:
        pass
    else:
        time_to_travel = abs(distance_mm) / speed_mm_s # in s
        turn_rate = omega_rad / time_to_travel # omega w

        # Left and right wheel speeds in steps/s
        left_mm_s = speed_mm_s - turn_rate * ( WHEEL_BASE_MM / 2 )
        right_mm_s = speed_mm_s + turn_rate * ( WHEEL_BASE_MM / 2 )

        # Velocities in steps/s
        left_steps_s = mm_to_steps(left_mm_s)
        right_steps_s = mm_to_steps(right_mm_s)

        # Distance moved with velocities found * time to travel ? 
        ### Need help with this one
        left_steps = left_steps_s * time_to_travel
        right_steps = right_steps_s * time_to_travel

        return (int(left_steps_s), int(right_steps_s), int(left_steps), int(right_steps))

def main():
    # Test case
    print(diff_drive_inverse_kin(130, 10, 0)) # should give (75, 75, 978, 978)
    print(diff_drive_inverse_kin(130, -10, 0)) # should give (-75, -75, 978, 978)
    print(diff_drive_inverse_kin(300, 50, 0)) # should give (376, 376, 2257, 2257)
    print(diff_drive_inverse_kin(200, 70, np.pi/4)) # should give (472, 582, 1348, 1661)
    print(diff_drive_inverse_kin(-200, 70, np.pi/4)) # should give (472, 582, 1348, 1661)
    print(diff_drive_inverse_kin(300, -40, -np.pi*2)) # should give (-134, -468, 1005, 3510)
    print(diff_drive_inverse_kin(0, 100, -np.pi*2)) # should give (753, -753, 1253, -1253)
    print(diff_drive_inverse_kin(0, 50, np.pi/2)) # should give (-376, 376, -313, 313)
    print(diff_drive_inverse_kin(0, -50, np.pi/2)) # should give (-376, 376, -313, 313)

if __name__ == '__main__':
    main()