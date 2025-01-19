import socket
import select
import epuck
import time

class EPuckIP(epuck.EPuck):

    ### Constants and commands specific to comport communication
    #Internal constants  
    _CMD_COMMAND_PACKET = 0x80
    _CMD_CAMERA_PACKET = 0x01
    _CMD_SENSOR_PACKET = 0x02
    _CMD_EMPTY_PACKET = 0x03
    _CMD_CAMERA_STREAM_BIT = 0x01
    _CMD_SENSORS_STREAM_BIT = 0x02
    
    #internal state
    _camera_enabled = False
    _sensors_enabled = False
    
    _isOpen = False  # IP doesn't have a clear concept of open/closed. We manage ourself and set to close on failure to push for reconnect

    def __init__(self, ip, port=1000, debug=False, timeout=10): #timeout in s  
        super().__init__(debug, timeout)
        self._port = port
        self._ip = ip 
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ### COMM methods
    def  _internal_connect(self):
        self._socket.connect( (self._ip, self._port) )
        self._isOpen = True; 
        #self._socket.settimeout(self._timeout)

    def is_connected(self):
        return self._isOpen

    def close(self):
        self._socket.close()
        self._isOpen = False

    def _dataAvailable(self):
        avail = select.select([self._socket], [], [self._socket], 0)  #poll mode
        return avail[0] != [] 

    def _writeData(self, packet):
        self._socket.sendall(packet)
 
    def _readData(self, size): #blocking
        data = bytearray()
        while len(data) < size:
            newData = self._socket.recv(size-len(data))
            if (len(newData) == 0):  # empty received data means closed port <-- not true when in non blocking
                self._isOpen = False
                return bytearray()
            data.extend(newData)
        return data
    
    ### Robot Level Commands   
    def set_camera_parameters(self, mode=epuck.CAM_MODE_RGB565, width=160, height=120, zoom=1):  
        self._debug_print("error- cannot set camera parameters in IP mode, ignoring")
    
    def get_camera_parameters(self):
        ## For IP connection camera is not configurable so we need to hard code the numbers
        (self.cam_mode, self.cam_width, self.cam_height, self.cam_zoom, self.cam_framebytes) = \
            (epuck.CAM_MODE_RGB565, 160, 120, 1, 38400)   ##QQVGA, zoom 1

    #override to fix IP protocol bug - If you start a song, the song will repeat the first note if you don't immediately send
    # a new packate with no song.
    def send_command(self):
        song_command = not (self.act_speaker_sound == epuck.SOUND_NOCHANGE or self.act_speaker_sound == epuck.SOUND_STOP)
        super().send_command()
        if (song_command): super().send_command()  #send again. it's automatically reset to no change by the super
        self._camera_enabled = self.enable_camera # remember our set state
        self._sensors_enabled = self.enable_sensors
      
    #overload, so that we empty the incoming stream as we send out the command.
    def stop_all(self):
        self.data_update()   # clear out the incoming cache
        super().stop_all()
        
          
    #request and update data on all active systems
    def data_update(self):
        
        if  ( (self.enable_camera != self._camera_enabled) or   #ensure requested streams match what user wants
            (self.enable_sensors != self._sensors_enabled) ):
            self.send_command()
            
    
        while (self._dataAvailable()):
            data = self._readData(1)  #get command byte
            match data[0]:
                case self._CMD_CAMERA_PACKET:
                    response = self._readData(self.cam_framebytes)
                    self.sens_framebuffer = response
                
                case self._CMD_SENSOR_PACKET:
                    response = self._readData(epuck._RESPONSE_PACKET_LEN)
                    self._parse_sensors_packet(response)
                
                case self._CMD_EMPTY_PACKET:
                    pass
                
                case _:
                    self._debug_print("unexpected packet signature "+str(data[0]))
    
    
    ### internal packet packing and unpacking methods
    # protocol taken from https://www.gctronic.com/doc/index.php?title=e-puck2_PC_side_development#WiFi_2
    def _make_command_packet(self):

        command_core = self._make_command_packet_core()
        request = 0x00
        if (self.enable_camera): request |= self._CMD_CAMERA_STREAM_BIT 
        if (self.enable_sensors): request |= self._CMD_SENSORS_STREAM_BIT 
        
        # add IP specific command header
        command = bytearray([
            self._CMD_COMMAND_PACKET,
            request
        ])
        command.extend(command_core)
        return command
    