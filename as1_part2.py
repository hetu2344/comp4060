from As1lib import *
import numpy as np
from math import *

WHEEL_BASE = 53 # in mm

def calc_R(left_mm, right_mm):
    
    return (left_mm + right_mm) / (right_mm - left_mm) * WHEEL_BASE / 2

def calc_icc_cordinates(rob_pos, r):
    x = rob_pos[0]
    y = rob_pos[1]
    theta = rob_pos[2]
    
    icc_x = x - (r * sin(theta))
    icc_y = y + (r * cos(theta))
    
    return (icc_x, icc_y)
    
def diff_linear_motion_kin(old_pos, distance_mm):
    x = old_pos[0]
    y = old_pos[1]
    theta = old_pos[2]
    
    new_x = x + distance_mm * cos(theta)
    new_y = y + distance_mm * sin(theta)
    
    return (new_x, new_y, theta)

def calc_omega(left_mm, right_mm):
    return (right_mm - left_mm) / WHEEL_BASE
    

def get_rotation_matrix(omega):
    matrix = [[cos(omega), -sin(omega), 0],
              [sin(omega),  cos(omega), 0],
              [0, 0, 1]]
    
    return np.array(matrix)

def get_icc_to_origin_vector(rob_pos, icc):
    vector = [[rob_pos[0] - icc[0]],    # x - icc_x
              [rob_pos[1] - icc[1]],    # y - icc_y
              [rob_pos[2]]]             # theta
    
    return np.array(vector)

def get_origin_to_icc_vector(icc, omega):
    vector = [[icc[0]],
              [icc[1]],
              [omega]]
    
    return np.array(vector)

def diff_drive_forward_kin(old_pos, left_steps, right_steps):
    # From old_pos figure ICC location
    # Then use the equation 5 from Computational Principles of Mobile Robotics
    # for calculating new position of robot
    left_mm = steps_to_mm(left_steps)
    right_mm = steps_to_mm(right_steps)
    
    if left_mm == right_mm:
        return diff_linear_motion_kin(old_pos, left_mm)
    
    r = calc_R(left_mm, right_mm)
    omega = calc_omega(left_mm, right_mm)
    
    icc_coor = calc_icc_cordinates(old_pos, r)
    
    rotation_matrix = get_rotation_matrix(omega)
    icc_to_orign_vec = get_icc_to_origin_vector(old_pos, icc_coor)
    origin_to_icc_vec = get_origin_to_icc_vector(icc_coor, omega)
    
    new_pos = (rotation_matrix.dot(icc_to_orign_vec)) + origin_to_icc_vec
    
    return (new_pos[0][0], new_pos[1][0], new_pos[2][0] % (2*math.pi))

# print_pose(diff_drive_forward_kin( (0, 0, 0), 0, 0)) # should give: (0, 0, 0)
# print_pose(diff_drive_forward_kin( (10, 20, 0), 1290, 1290)) # should give: (178, 20, 0)
# print_pose(diff_drive_forward_kin( (10, 20, np.pi/2), 1290, 1290)) # should give: (10, 188, 90)
# print_pose(diff_drive_forward_kin( (0, 0, 0), -1290, 1290)) #should give (0,0,0)
# print_pose(diff_drive_forward_kin( (0, 0, np.pi/2), 1290, -1290)) #should give (0, 0, 90)
# print_pose(diff_drive_forward_kin( (0, 0, 0), 2580, 0)) #should give (0, 0, 0)
# print_pose(diff_drive_forward_kin( (1000, 1000, np.pi/2), 1290, -1290)) #should give (1000, 1000, 90)
# print_pose(diff_drive_forward_kin( (0, 0, np.pi/2), 1290, 100)) #should give (62, 7, 283)
# print_pose(diff_drive_forward_kin( (0, 0, 0), 1991, 2075)) #should give (263,27, 12)
# print_pose(diff_drive_forward_kin( (0, 0, 0), 189, 2422)) #should give (-23,10, 312)
# print_pose(diff_drive_forward_kin( (0, 0, 0), 1249, 2598)) #should give (-11,152, 188)
