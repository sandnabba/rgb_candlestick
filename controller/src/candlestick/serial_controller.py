from serial import Serial, serialutil
import logging

class SerialController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initiating Serial controller")
        self.serial_port = "/dev/ttyUSB0"
        self.led = [[0, 0, 0] for _ in range(7)]
        try:
            self.ser = Serial(self.serial_port, 57600)
            self.serial_connected = True
            self.logger.debug("Connected to serial port: %s", self.serial_port)
        except serialutil.SerialException:
            self.logger.critical("Could not open serial port, printing values to screen instead")
            self.serial_connected = False

    def commit_arr(self, direction=None):
        #self.logger.debug("Commiting array, direction: %s", direction)
        # Array sent to Arduino:
        if not direction or direction == "right":
            values = [
                self.led[i][j]
                for i in range(7)  # Rows 0 through 6
                for j in range(3)  # Columns 0 through 2
            ]
        elif direction == "left":
            values = [
                self.led[i][j]
                for i in range(6, -1, -1)  # Rows 6 through 0 (reversed)
                for j in range(3)          # Columns 0 through 2
            ]
        elif direction == "down":
            values = [
                self.led[i][j]
                for i in [3, 2, 1, 0, 1, 2, 3]
                for j in range(3)
            ]
        elif direction == "up":
            values = [
                self.led[i][j]
                for i in [0, 1, 2, 3, 2, 1, 0]
                for j in range(3)
            ]

        if self.serial_connected:
            self.serial_write(values)
        else:
            self.logger.debug(values)

    def serial_write(self, values):
        while self.ser.in_waiting:
            response = self.ser.readline()
            print("Response: ", response)
            sleep(0.02)
        values.insert(0, 255)
        values.append(254)
        self.ser.write(bytearray(values))
        while self.ser.in_waiting:
            response = self.ser.readline()
            print("Response: ", response)
            sleep(0.02)

    def set_full_array(self, values, direction=None):
        self.led = values
        self.commit_arr(direction)

    def set_led(self, x, color, send=True, direction=None):
        self.logger.debug("Setting led %s, direction: %s", x, direction)
        self.led[x] = color
        if send:
            self.commit_arr(direction)

    def set_all(self, color=None):
        '''
        Set all LEDs to the same color.
        '''
        for i in range(7):
            self.led[i] = color
        self.commit_arr("right")
