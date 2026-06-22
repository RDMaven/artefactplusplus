from MPU6050 import *

accel_x_bias, accel_x_noise, accel_y_bias, accel_y_noise, accel_z_bias, accel_z_noise, gyro_x_bias, gyro_x_noise, gyro_y_bias, gyro_y_noise, gyro_z_bias, gyro_z_noise = getInfo()

R = np.diag([accel_x_bias, accel_x_noise, accel_y_bias, accel_y_noise, accel_z_bias, accel_z_noise, gyro_x_bias, gyro_x_noise, gyro_y_bias, gyro_y_noise, gyro_z_bias, gyro_z_noise])

print(R)










