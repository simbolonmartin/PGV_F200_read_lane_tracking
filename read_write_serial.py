import serial
import time

array = []
def requestBlue():
    global array
    array.clear()
    
    array.append(0x3B) #1
    array.append(0xC4) #0


    array_send = bytearray(array)

    return array_send
# Configure the serial port
ser = serial.Serial('COM5', baudrate=115200, timeout=1)  # Replace 'COM1' with your serial port name

def read_serial():
    if ser.is_open:
        try:
            data = ser.read(21)  # Read 21 bytes of data
            return data.hex()    # Convert the bytes to a hexadecimal string
        except Exception as e:
            print(f"Error reading from serial port: {e}")
    else:
        print("Serial port is not open.")

def write_serial(data):
    if ser.is_open:
        try:
            # hex_data = bytes.fromhex(data)  # Convert the hexadecimal string to bytes
            hex_data = data
            ser.write(hex_data)
            print(f"Sent: {hex_data.hex()}")
        except Exception as e:
            print(f"Error writing to serial port: {e}")
    else:
        print("Serial port is not open.")

if __name__ == "__main__":
    # ser.open()
    
    if ser.is_open:
        try:
            while True:
                # command = input("Enter a command (2 bytes in hex) to send via serial port (or 'exit' to quit): ")
                command = requestBlue()
                # if command.lower() == 'exit':
                #     break
                
                # if len(command) != 4:  # Check if the input is exactly 4 characters (2 bytes in hex)
                #     print("Please enter a valid 2-byte hex command.")
                #     continue
                
                write_serial(command)
                # time.sleep(0.1)
                response = read_serial()
                print(f"Received: {response}")
        except KeyboardInterrupt:
            pass  # Allow for a graceful exit using Ctrl+C
        finally:
            ser.close()
    else:
        print("Failed to open serial port.")
