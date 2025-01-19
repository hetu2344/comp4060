import time
import random
from epuck_com import EPuckCom
from epuck_ip import EPuckIP
import epuck  #for user constants

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def cam_bytes_to_image(mode, data, width, height):

    if (mode == epuck.CAM_MODE_RGB565):
        npdata = np.frombuffer(data, dtype=">i2")    # camera is big endian, 16 bit per pixel.
        npdata = npdata.astype(np.uint32)            #expand to 32 bit to make room for unpacking.
        alpha = 0xFF000000     #ALPHA is MSB, all set to 1
        r = ((npdata & 0xF800) >> 8)    # mask out top 5 bits, then shift right to make it the LSB of the 32 bit
        g = ((npdata & 0x07E0) << 5)         # mask out middle 6 bits, then shift a little left to make it the 2nd LSB
        b = ((npdata & 0x001F) << 19)        # mask out the bottom 5 bits, then shift it all the way left to be the 3rd LSB
        arr = alpha + r + g + b
        return Image.frombuffer('RGBA', (width, height), arr, 'raw', 'RGBA', 0, 1)  

    if (mode == epuck.CAM_MODE_GREY):
        npdata = np.frombuffer(data, np.uint8)    # camera is big endian, 16 bit per pixel.
        return Image.frombuffer('L', (width, height), npdata, 'raw', 'L', 0, 1)    

def epuck_test():
    # /dev/tty.e-puck2_05798
    # /dev/cu.e-puck2_05798
    epuckcomm = EPuckCom("/dev/cu.usbmodem3011", debug=True)
    # epuckcomm = EPuckCom("/dev/cu.e-puck2_05798", debug=True)
    # epuckcomm = EPuckIP("192.168.229.106", debug=True)
    if (not epuckcomm.connect()):
        print("Could not connect, quitting")
        return

    epuckcomm.enable_sensors = True
    #epuckcomm.enable_camera = True
    epuckcomm.send_command() # enable sensor stream.
    time.sleep(0.5)  #give time for the robot to get the request

    # epuckcomm.set_camera_parameters(epuck.CAM_MODE_RGB565, 40, 40, 1)
    # epuckcomm.set_camera_parameters(EPuckComm.CAM_MODE_GREY, 40, 40, 8)
    epuckcomm.get_camera_parameters()
    print(epuckcomm.cam_framebytes)

    #epuckcomm.act_speaker_sound = epuck.SOUND_STARWARS
    # epuckcomm.send_command()
    # time.sleep(5)

    for i in range(100):
        epuckcomm.state.act_binary_led_states[random.randint(0,epuck.BINARY_LED_COUNT-1)] = random.randint(0,1)
        epuckcomm.state.act_rgb_led_colors[random.randint(0,epuck.RGB_LED_COUNT-1)] = (random.randint(0,100), random.randint(0,100), random.randint(0,100))
        epuckcomm.state.act_left_motor_speed = 1200
        epuckcomm.state.act_right_motor_speed = -1200
        # epuckcomm.send_command()
        epuckcomm.data_update()
        
        if (epuckcomm.enable_camera):
            im = cam_bytes_to_image(epuckcomm.cam_mode, epuckcomm.sens_framebuffer, epuckcomm.cam_width, epuckcomm.cam_height)
            if (epuckcomm.cam_mode == epuck.CAM_MODE_GREY):
                plt.imshow(im, cmap='gray', vmin=0, vmax=255)
            elif (epuckcomm.cam_mode == epuck.CAM_MODE_RGB565): 
                plt.imshow(im)
            plt.pause(0.000001)
        
        print(str(epuckcomm.state.sens_tof_distance_mm) + " steps L/R: "+ str(epuckcomm.state.sens_left_motor_steps) + "/" + str(epuckcomm.state.sens_right_motor_steps))
        time.sleep(0.1) #100hz roughly
    time.sleep(2)

    epuckcomm.stop_all()
    epuckcomm.close()
    
    
epuck_test()
