std_msgs/Header header

uint32 seq

float32 t_csv

# Driver inputs / states
float32 steering_angle
float32 brake_pressure
float32 accel_opening
float32 torque_request
bool ready_to_drive

# Powertrain
float32 motor_temperature
float32 motor_rpm
float32 inverter_voltage
float32 igbt_temperature

# Suspension strokes
float32 stroke_rr
float32 stroke_rl
float32 stroke_fr
float32 stroke_fl

# GPS
float64 longitude
float64 latitude

# IMU
float32 gyro_x
float32 gyro_y
float32 gyro_z
