import serial
import time

class PGVCommunication():
       
    def __init__(self) -> None:
        self.usb_port = "COM5"
        self.baud_rate = 115200
        self.check_connection()
        self.initialize_message()

    def check_connection(self):
        try:
            self.serial_channel = serial.Serial(self.usb_port, self.baud_rate, timeout=3, parity=serial.PARITY_EVEN)
            print("Serial details params: ", self.serial_channel)
        except:
            print("Couldn't connect to usb port")

    def initialize_message(self):
        self.position_value = [0xC8, 0x37]
        self.request_blue = [0xC4, 0x3B]
        self.request_green = [0x88, 0x77]
        self.request_red = [0x90, 0x6F]

    def send_message(self, message):
        """Send message to the PGV

        Args:
            message (hex): the message that will be sent to the PGV
        """
        self.result_write = self.serial_channel.write(message)
        # print(f'result_write: {self.result_write}')

    def read_message(self):
        # print("reading message")
        self.result_read = self.serial_channel.read(21)
        # self.result_read_hex =self.result_read.hex()
        # print(f'result_read: {self.result_read}')
        # print(f'hex access index 0: {repr(chr(self.result_read[0]))}')
        # print(f'hex access index 1: {self.result_read[1]}')
        # print(f'hex access index -1: {self.result_read[-1]}')
        # print(f'length: {len(self.result_read_hex)}')
    
    def print_result_read(self):
        counter = 1
        for _ in self.result_read:
            print(f'{counter}  = {_}')
            if counter == 2:
                print(f"binary representation: {bin(_)[2:].zfill(8)}")
            counter += 1

    def calculate(self):
        """Calculate the angle value, y_position, and number of lanes detected.
        """
        multiplier = 0x80
        byte_2_binary = bin(self.result_read[1])[2:].zfill(8)
        # print(f"len binary =  {len(byte_2_binary)}")
        # print(f"index_2 =  {byte_2_binary[2]}")
        # print(f"index_2 =  {byte_2_binary[3]}")
        self.number_of_lanes = int(byte_2_binary[2]) * 2 + int(byte_2_binary[3])
        # print(f'number_of_lanes: {number_of_lanes}')
        self.angle_value = self.result_read[10] * multiplier + self.result_read[11]
        if self.angle_value > 180 :
            self.angle_value = - (360-self.angle_value)
        y_position_unsigned = self.result_read[6] * multiplier + self.result_read[7]
        if y_position_unsigned > 0x2000:
            self.y_position = -1 * int(0x4000 - y_position_unsigned)
        else:
            self.y_position = int(y_position_unsigned)
        self.tracking_result = [self.number_of_lanes, self.angle_value, self.y_position]

    def stream_value(self):
        """View all the tracking lane values information (angle_value, y_position, number_of_lanes)
        """
        try:
            while True:
                self.send_message(self.position_value)
                self.read_message()
                self.calculate()
                # self.print_result_read()
                # print(f'angle_value: {self.angle_value} \t y_position: {self.y_position} \t number_of_lanes: {self.number_of_lanes}') #TODO: comment this on deployment
                time.sleep(0.1) #TODO: check this if it is enough to have a good movement result
        except Exception as error:
            print (error)
        finally:
            self.serial_channel.close()

    def update_value(self):
        try:
            self.send_message(self.position_value)
            self.read_message()
            self.calculate()
            time.sleep(0.1)
        except Exception as error:
            print(error)
        
    


if __name__ == "__main__":
    PGVCommunicationObject = PGVCommunication()
    PGVCommunicationObject.stream_value()
    # PGVCommunicationObject.print_result_read()