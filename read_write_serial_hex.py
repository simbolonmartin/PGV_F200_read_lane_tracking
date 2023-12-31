import time
import serial


class PGVCommunication:
    def __init__(self) -> None:
        # self.usb_port = "/dev/ttyUSB1"
        # self.usb_port = "COM3" #for Windows
        self.usb_port = "/dev/pgv_sensor"  # for Ubuntu
        self.baud_rate = 115200
        self.result_write = None
        self.result_read = None
        self.number_of_lanes = None
        self.angle_value = None
        self.y_position = None
        self.tracking_result = None
        self.check_connection()
        self.initialize_message()
        self.trigger_sensor()

    def check_connection(self):
        try:
            self.serial_channel = serial.Serial(
                self.usb_port, self.baud_rate, timeout=3, parity=serial.PARITY_EVEN
            )
            # print("Serial details params: ", self.serial_channel)
        except:
            print("Couldn't connect to usb port")

    def initialize_message(self):
        self.position_value = [0xC8, 0x37]
        self.request_blue = [0xC4, 0x3B]
        self.request_green = [0x88, 0x77]
        self.request_red = [0x90, 0x6F]
        self.follow_left_lane = [0xE8, 0x17]

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
            print(f"{counter}  = {_}")
            if counter == 2:
                print(f"binary representation: {bin(_)[2:].zfill(8)}")
            counter += 1

    def calculate(self):
        """Calculate the angle value, y_position, and number of lanes detected."""
        multiplier = 0x80
        byte_2_binary = bin(self.result_read[1])[2:].zfill(8)
        # print(f"len binary =  {len(byte_2_binary)}")
        # print(f"index_2 =  {byte_2_binary[2]}")
        # print(f"index_2 =  {byte_2_binary[3]}")
        self.number_of_lanes = int(byte_2_binary[2]) * 2 + int(byte_2_binary[3])
        # print(f'number_of_lanes: {self.number_of_lanes}')
        self.angle_value = self.result_read[10] * multiplier + self.result_read[11]
        if self.angle_value > 180:
            self.angle_value = -(360 - self.angle_value)
        y_position_unsigned = self.result_read[6] * multiplier + self.result_read[7]
        if y_position_unsigned > 0x2000:
            self.y_position = -1 * int(0x4000 - y_position_unsigned)
        else:
            self.y_position = int(y_position_unsigned)
        self.tracking_result = [self.number_of_lanes, self.angle_value, self.y_position]
        # print(self.tracking_result)

    def trigger_sensor(self):
        """The sensor needs to be triggered first by sending color request and follow_left_lane message"""
        try:
            self.send_message(self.request_blue)
            time.sleep(0.1)
            self.send_message(self.follow_left_lane)
            time.sleep(1)
        except Exception as error:
            print(error)
        finally:
            self.serial_channel.close()
            time.sleep(1)
            self.check_connection()
            time.sleep(1)

    def stream_value(self):
        """View all the tracking lane values information (angle_value, y_position, number_of_lanes)"""
        try:
            # self.send_message(self.request_blue)
            # time.sleep(0.1)
            # self.send_message(self.follow_left_lane)
            # time.sleep(3)
            while True:
                self.update_value()
                if __name__ == "__main__":
                    print(
                        f"number_of_lanes: {self.number_of_lanes} \t angle_value: {self.angle_value} \t y_position: {self.y_position}"
                    )
        except Exception as error:
            print(error)
        finally:
            self.serial_channel.close()

    def update_value(self):
        """Will calculate the tracking result with delay 0.1 for each call"""
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
