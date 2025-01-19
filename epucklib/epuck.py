import struct
from abc import ABC, abstractmethod
import time
from epucklib.epuck_state import *

###Constants for user use
CAM_MODE_RGB565 = 1
CAM_MODE_GREY = 0
    
#internal constants
_RESPONSE_PACKET_LEN = 104

class EPuck(ABC):
    ###Public state variables for external use

    #library state variables
    enable_camera = False     #when enabled, requests and gets camera frame each update.
    enable_sensors = False     #when enabled, requests and gets camera frame each update.

    state = EPuckState()

    def __init__(self, debug=False, timeout=4):  #timeout in s
        self._debug = debug
        self._timeout = timeout

    def __str__(self):
        return str(self.state)

    def _debug_print(self, msg):
        if(self._debug): print(self.__class__.__name__+": "+msg)

    ### COMM methods
    def connect(self):
        self._debug_print("attempting to connect")
        if (not self._internal_connect()):   
            self._debug_print("failed to connect")
            return False
        self._debug_print(f"connected")
        return True

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def close(self):
        pass
    
    #send a robot command using the configured state variables
    def send_command(self):
        self._debug_print("sending command")
        self._writeData(self._make_command_packet())
        self._debug_print("command sent")
        self.act_speaker_sound = SOUND_NOCHANGE #to avoid re-starting sound each time, only do once.
        
    #stop motion, sound, etc.
    def stop_all(self):
        self.state.stop_all()
        self._debug_print("issuing stop command")
        self.send_command()
        time.sleep(2)  #add a sleep because its common to just close after before the buffer is clear
    
    ### Com method specific commands
    
    #do whatever is needed to update data based on the com method
    @abstractmethod
    def data_update(self):
        pass
    
    @abstractmethod
    def _internal_connect(self):
        pass
    
    @abstractmethod
    def _writeData(self, packet):
        pass

    @abstractmethod
    def _readData(self, size):
        pass
    
    ### Robot Level Commands
    @abstractmethod   
    def get_camera_parameters(self):
        pass
    
    @abstractmethod     
    def set_camera_parameters(self, mode=CAM_MODE_RGB565, width=160, height=120, zoom=1):  
        pass  
    
    ### internal packet packing and unpacking methods
    # protocol taken from https://www.gctronic.com/doc/index.php?title=e-puck2_PC_side_development#WiFi_2

    @abstractmethod
    def _make_command_packet(self):
        pass

    def _make_command_packet_core(self):

        ### You can send whatever commands you want. In this comm package, we request a state update and immediately
        # send a command packet with all the actuators, as a set.
        # it doesn't need to be this way, you can just get sensors or actuators or a subset (see docs as per above)

        #convert motor speeds to 16 bit little endian
        left_motor_speed = struct.pack('<h', int(self.state.act_left_motor_speed))
        right_motor_speed = struct.pack('<h', int(self.state.act_right_motor_speed))

        led_bits = 0x00
        for i in range(BINARY_LED_COUNT):
            if self.state.act_binary_led_states[i]: led_bits = led_bits | (1 << i)

        command = bytearray([
            0,		                        # don't bother with settings, check docs for options
            left_motor_speed[0],		    # left motor speed LSB
            left_motor_speed[1],		    # left motor speed MSB
            right_motor_speed[0],		    # right motor speed LSB
            right_motor_speed[1],		    # right motor speed MSB
            led_bits,	                    # binary LEDs
            self.state.act_rgb_led_colors[0][R],		# LED2 red
            self.state.act_rgb_led_colors[0][G],		# LED2 green
            self.state.act_rgb_led_colors[0][B],	    # LED2 blue
            self.state.act_rgb_led_colors[1][R],		# LED4 red
            self.state.act_rgb_led_colors[1][G],		# LED4 green
            self.state.act_rgb_led_colors[1][B],	    # LED4 blue
            self.state.act_rgb_led_colors[2][R],		# LED6 red
            self.state.act_rgb_led_colors[2][G],		# LED6 green
            self.state.act_rgb_led_colors[2][B],	    # LED6 blue
            self.state.act_rgb_led_colors[3][R],		# LED8 red
            self.state.act_rgb_led_colors[3][G],		# LED8 green
            self.state.act_rgb_led_colors[3][B],	    # LED8 blue
            self.state.act_speaker_sound	# speaker
        ])
        return command
    
    def _parse_sensors_packet(self, response):
        # print(response)
        data = struct.unpack("<"+   #epuck is in little endian
                "3h"+  #accelerometer xes X Y Z
                "3f"+  #acceleration, orientation, inclination
                "3h"+   #gyro X Y Z axis values
                "3f"+   #magnetometer X Y Z axes
                "B"+   #Temperature in c
                "HHHHHHHH"+ #proximity sensors
                "HHHHHHHH"+ #ambient light sensors
                "H"+    #tof
                "HHHH" +    #microphones
                "HH" +   #motors L/R
                "H"  +   #battery level
                "?"  +   #SD present
                "xxx" +  # Rc5 TV protocol, ignored
                "B" +   #selector
                "HHH" + #ground proximity
                "HHH" +  #ground ambient
                "?"   +  #button
                "B",
                response)
        self.state.load_data(data)


