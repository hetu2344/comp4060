
#constants for readibility sanity
R = X = 0
G = Y = 1
B = Z = 2

###Constants for user use
BINARY_LED_COUNT = 6   #binary leds
BINARY_LED_1 = 0  #indices into LED array
BINARY_LED_3 = 1
BINARY_LED_5 = 2
BINARY_LED_7 = 3
BINARY_LED_BODY = 4
BINARY_LED_FRONT = 5
    
RGB_LED_COUNT = 4
RGB_LED_2 = 0
RGB_LED_4 = 1
RGB_LED_6 = 2
RGB_LED_8 = 3

SOUND_NOCHANGE = 0x00
SOUND_MARIO = 0x01
SOUND_UNDERWORLD = 0x02
SOUND_STARWARS = 0x04
SOUND_4Khz = 0x08
SOUND_10khz = 0x10
SOUND_STOP = 0x20

SENS_PROXIMITY_COUNT = 8
SENS_AMBIENT_COUNT = SENS_PROXIMITY_COUNT
SENS_MIC_COUNT = 4
SENS_GROUND_PROX_COUNT = 3
SENS_GROUND_AMB_COUNT = SENS_GROUND_PROX_COUNT

#ground sensor indices
SENS_GROUND_LEFT = 0
SENS_GROUND_CENTER = 1
SENS_GROUND_RIGHT = 2

#proximity sensor indices
(SENS_PROX_R_10,    #10 degrees on right
 SENS_PROX_R_45,    
 SENS_PROX_R_90,
 SENS_PROX_R_135,
 SENS_PROX_L_135,    #10 degrees on left of center
 SENS_PROX_L_90,    
 SENS_PROX_L_45,
 SENS_PROX_L_10) = range(SENS_PROXIMITY_COUNT)

class EPuckState():

    #actuators to set
    act_left_motor_speed = 0  # -1000..1000, steps / second?
    act_right_motor_speed = 0
    act_binary_led_states = [False]*BINARY_LED_COUNT
    act_rgb_led_colors = [ (0,0,0) ]*RGB_LED_COUNT
    act_speaker_sound = SOUND_STOP
    
    ## things to read
    sens_framebuffer = None
    sens_accelerometer = [0, 0, 0]  #X Y Z
    sens_acceleration = 0
    sens_orientation = 0
    sens_inclination = 0
    sens_gyro = [0, 0, 0] #X Y Z
    sens_magnetometer = [0, 0, 0] #X Y Z
    sens_temperature = 0
    sens_proximity = [0]*SENS_PROXIMITY_COUNT
    sens_ambient = [0]*SENS_AMBIENT_COUNT
    sens_tof_distance_mm = 0
    sens_mic_volume = [0]*SENS_MIC_COUNT
    sens_left_motor_steps = 0
    sens_right_motor_steps = 0
    sens_battery_mv = 0
    sens_has_SD = False
    sens_selector_pos = 0
    sens_ground_prox = [0]*SENS_GROUND_AMB_COUNT
    sens_ground_amp = [0]*SENS_GROUND_AMB_COUNT
    sens_button_press = False

    #camera parameters loaded from robot/library
    cam_mode = -1
    cam_width = -1
    cam_height = -1
    cam_zoom = -1
    cam_framebytes = -1

    def __init__(self): 
        pass

    def __str__(self):
        ##column widths for auto alignment
        col1 =  4
        col2 = 15
        col3 = 8
        col4 = col3
        col5 = col3
        prec = 2  #precision of floats

        output = f"""
        ----
        Sensor state:
        {"":<{col1}} {"accelerometer":>{col2}} x: {self.sens_accelerometer[X]:<{col3}} y: {self.sens_accelerometer[Y]:<{col4}} z: {self.sens_accelerometer[Z]}
        {"":<{col1}} {"acceleration":>{col2}} {self.sens_acceleration:<{col3}}
        {"":<{col1}} {"orientation":>{col2}} {str(self.sens_orientation,)+"°":<{col3}}
        {"":<{col1}} {"inclination":>{col2}} {str(self.sens_inclination)+"°":<{col3}}
        {"":<{col1}} {"gryo":>{col2}} x: {self.sens_gyro[X]:<{col3}} y: {self.sens_gyro[Y]:<{col4}} z: {self.sens_gyro[Z]}
        {"":<{col1}} {"magnetometer":>{col2}} x: {self.sens_magnetometer[X]:<{col3}.{prec}} y: {self.sens_magnetometer[Y]:<{col4}.{prec}} z: {self.sens_magnetometer[Z]}
        {"":<{col1}} {"temperature":>{col2}} {str(self.sens_temperature)+"c":<{col3}}
        {"":<{col1}} {"proximity":>{col2}} 1: {self.sens_proximity[0]:<{col3}} 2: {self.sens_proximity[1]:<{col4}} 3: {self.sens_proximity[2]:<{col5}} 4: {self.sens_proximity[3]}
        {"":<{col1}} {"-":>{col2}} 5: {self.sens_proximity[4]:<{col3}} 6: {self.sens_proximity[5]:<{col4}} 7: {self.sens_proximity[6]:<{col5}} 8: {self.sens_proximity[7]}
        {"":<{col1}} {"ambient prox":>{col2}} 1: {self.sens_ambient[0]:<{col3}} 2: {self.sens_ambient[1]:<{col4}} 3: {self.sens_ambient[2]:<{col5}} 4: {self.sens_ambient[3]}
        {"":<{col1}} {"-":>{col2}} 5: {self.sens_ambient[4]:<{col3}} 6: {self.sens_ambient[5]:<{col4}} 7: {self.sens_ambient[6]:<{col5}} 8: {self.sens_ambient[7]}
        {"":<{col1}} {"time of flight dist":>{col2}} {str(self.sens_tof_distance_mm)+"mm":<{col3}}
        {"":<{col1}} {"mic":>{col2}} 1: {self.sens_mic_volume[0]:<{col3}} 2: {self.sens_mic_volume[1]:<{col4}} 3: {self.sens_mic_volume[2]:<{col5}} 4: {self.sens_mic_volume[3]}
        {"":<{col1}} {"motor steps":>{col2}} l: {self.sens_left_motor_steps:<{col3}} r: {self.sens_right_motor_steps:<{col4}}
        {"":<{col1}} {"battery":>{col2}} {str(self.sens_battery_mv)+"mv":<{col3}}
        {"":<{col1}} {"SD card":>{col2}} {str(self.sens_has_SD):<{col3}}
        {"":<{col1}} {"selector pos.":>{col2}} {str(self.sens_selector_pos)+"mv":<{col3}}
        {"":<{col1}} {"ground prox":>{col2}} 1: {self.sens_ground_prox[0]:<{col3}} 2: {self.sens_ground_prox[1]:<{col4}} 3: {self.sens_ground_prox[2]:<{col5}} 
        {"":<{col1}} {"groung amb prox":>{col2}} 1: {self.sens_ground_amp[0]:<{col3}} 2: {self.sens_ground_amp[1]:<{col4}} 3: {self.sens_ground_amp[2]:<{col5}}
        {"":<{col1}} {"button":>{col2}} {str(self.sens_button_press):<{col3}}

        """

        return output
    
    def stop_all(self):
        self.enable_camera = self.enable_sensors = False
        self.act_left_motor_speed = 0 
        self.act_right_motor_speed = 0
        self.act_binary_led_states = [False]*BINARY_LED_COUNT
        self.act_rgb_led_colors = [ (0,0,0) ]*RGB_LED_COUNT
        self.act_speaker_sound = SOUND_STOP


    def load_data(self, data):   # load data from a tuple representing all the sensors, in order of the com protocol, into variables. 
            self.sens_accelerometer[X], self.sens_accelerometer[Y], self.sens_accelerometer[Z], \
            self.sens_acceleration, self.sens_orientation, self.sens_inclination, \
            self.sens_gyro[X], self.sens_gyro[Y], self.sens_gyro[Z], \
            self.sens_magnetometer[X], self.sens_magnetometer[Y], self.sens_magnetometer[Z], \
            self.sens_temperature, \
            self.sens_proximity[0], self.sens_proximity[1], self.sens_proximity[2], self.sens_proximity[3], \
            self.sens_proximity[4], self.sens_proximity[5], self.sens_proximity[6], self.sens_proximity[7], \
            self.sens_ambient[0], self.sens_ambient[1], self.sens_ambient[2], self.sens_ambient[3], \
            self.sens_ambient[4], self.sens_ambient[5], self.sens_ambient[6], self.sens_ambient[7], \
            self.sens_tof_distance_mm, \
            self.sens_mic_volume[0], self.sens_mic_volume[1], self.sens_mic_volume[2], self.sens_mic_volume[3], \
            self.sens_left_motor_steps, self.sens_right_motor_steps, \
            self.sens_battery_mv, \
            self.sens_has_SD, \
            self.sens_selector_pos, \
            self.sens_ground_prox[0], self.sens_ground_prox[1], self.sens_ground_prox[2], \
            self.sens_ground_amp[0], self.sens_ground_amp[1], self.sens_ground_amp[2], \
            self.sens_button_press, dummy = data