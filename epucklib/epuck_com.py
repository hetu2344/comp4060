import epucklib.epuck as epuck
import serial

class EPuckCom(epuck.EPuck):
    ### Constants and commands specific to comport communication
    #Internal constants  
    _MAX_READLINE = 256
    _CAM_HEADER_BYTES = 3   #mode, width, height

    #binary mode commands
    _CMD_GET_ALL_SENSORS = 0xF8
    _CMD_SET_ALL_ACTUATORS = 0xF7
    _CMD_GET_CAM_FRAME = 0xB7

    #ascii mode commands
    _CMD_GET_CAM_PARAMETERS = 'I'
    _CMD_SET_CAM_PARAMETERS = 'J'


    def __init__(self, port, baud=115200, debug=False, timeout=4):  #timeout in s
        super().__init__(debug, timeout)
        self._port = port
        self._baud = baud
 

    ### COMM methods
    def  _internal_connect(self):
        try:
            self._s_com = serial.Serial(self._port, self._baud, timeout=self._timeout)
        except Exception as error:
            print(error)
            self._s_com = None
            return False
        return True

    def is_connected(self):
        return self._s_com.is_open()

    def close(self):
        self._s_com.close()

    def _writeData(self, packet):
        self._s_com.write(packet)

    def _readData(self, size): #blocking
        return self._s_com.read(size)

    ### Robot Level Commands
    #set camera parameters: mode(0=grayscale, 1=rgb565), width=[1...640], height=[1...480], zoom=[1,2,4,8], x=[1...640], y=[1...480]
    def set_camera_parameters(self, mode=epuck.CAM_MODE_RGB565, width=40, height=40, zoom=1, x=-1, y=-1):  # note: use of x,y is not clear, I ignore
        if (x==-1): x=width
        if (y==-1): y=width
        command_string = f"{self._CMD_SET_CAM_PARAMETERS},{mode},{width},{height},{zoom},{x},{y}\n" 

        self._debug_print("setting camera parameters")
        self._writeData(command_string.encode("ascii"))
        self._debug_print("command sent, waiting for response")
        response = self._readData(self._MAX_READLINE)
        if (response[0] != ord('j')):
            print("ERR unexpected character returned from ascii command")

    def get_camera_parameters(self):
        command_string = self._CMD_GET_CAM_PARAMETERS+"\n"

        self._writeData(command_string.encode("ascii"))
        response = self._s_com.readline(self._MAX_READLINE)  ##ascii mode, don't use _readData
        raw_data = response.decode("utf_8").rstrip().split(',')
        if (response[0] != ord('i')):
            print("ERR unexpected character returned from ascii command")
        (self.cam_mode, self.cam_width, self.cam_height, self.cam_zoom, self.cam_framebytes) = tuple(map(int,raw_data[1:]))
     
    #For COM the command may include a request for data which we should get right away.
    #overload to just do a data update.
    def send_command(self):
        self.data_update()
                  
    def data_update(self):  #request data and get it
        super().send_command() # send request for data
        
        if (self.enable_sensors):  # above send?command already requested sensor data.
            self._debug_print("waiting for data")
            response = self._readData(size=epuck._RESPONSE_PACKET_LEN-1) # -1 for reserved byte. seems to not show up on com
            response += b'0'  #pad the reserved end byte
            # stri = "length of response = " + str(len(response))
            # self._debug_print(stri)
            self._debug_print("response received, parsing")
            self._parse_sensors_packet(response)
            self._debug_print("parsing complete, update complete")
            
        if(self.enable_camera):
            if (self.cam_framebytes == -1): # camera parameters not yet received
                self._debug_print("first getting camera parameters")
                self.get_camera_parameters()
                
            self.sens_framebuffer = response = self._get_cam_frame()



    def _get_cam_frame(self):  #sends command to request camera frame and parses repsonse
        self._debug_print("sending command to request camera frame")
        self._writeData(
            bytearray([
                self._CMD_GET_CAM_FRAME,
                0   # command ends in null
            ])
        )
        self._debug_print("command sent, waiting for response")
        response = self._readData(size=(self.cam_framebytes+self._CAM_HEADER_BYTES))
        self._debug_print("image received. Mode "+ str(response[0]) + "  width: "+ str(response[1])+ " height: "+str(response[2]))
        imgarr = response[self._CAM_HEADER_BYTES:]
        self._debug_print("parsing complete, update complete")
        return imgarr

    ### internal packet packing and unpacking methods
    # protocol taken from https://www.gctronic.com/doc/index.php?title=e-puck2_PC_side_development#WiFi_2

    def _make_command_packet(self):

        command_core = self._make_command_packet_core()
        
        # add COM specific command header
        command = bytearray()
        if (self.enable_sensors): command.extend( bytearray([self._CMD_GET_ALL_SENSORS]))
        command.extend( bytearray([self._CMD_SET_ALL_ACTUATORS]) )
        command.extend(command_core)
        
        # add COM specific null termination
        command.extend(bytearray ([0]))
        return command
    



