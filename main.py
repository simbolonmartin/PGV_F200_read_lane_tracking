from read_write_serial_hex import PGVCommunication

PGV = PGVCommunication()

velocity = 0
rotation_speed = 0 

def steering_wheel_controller(number_of_lanes:int, angle_value:int, y_position:int):
    global velocity, rotation_speed
    Kp = 0.01
    Ki = 0
    Kd = 0
    if number_of_lanes != 1:
        # print(f'{number_of_lanes} lane(s) are detected. It has to be 1')
        velocity = 0.05
        rotation_speed = 0 
    else:
        if angle_value == 0:
            velocity = 0.05
            rotation_speed = 0 
        else:
            velocity = 0.03    
            rotation_speed = - Kp * angle_value
    # print(f"velocity: {velocity} \t rotation_speed {rotation_speed}")


for a in range(0,1000):
    PGV.update_value()   #TODO: make this a thread?
    steering_wheel_controller(PGV.number_of_lanes, PGV.angle_value, PGV.y_position)
    print(f'number_of_lanes: {PGV.number_of_lanes} \t angle_value: {PGV.angle_value} \t y_position: {PGV.y_position} \t velocity: {velocity} \trotation_speed: {rotation_speed}')

        








