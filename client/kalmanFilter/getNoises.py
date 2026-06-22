import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import numpy as np

# Create an MPU9250 instance
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=0x68,  # In case the MPU9250 is connected to another I2C device
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)


from smbus2 import SMBus

bus = SMBus(1)

whoami = bus.read_byte_data(0x68, 0x75)

print(hex(whoami))

# Configure seulement gyro + accel
mpu.configureMPU6500(GFS_1000, AFS_8G)

def getInfo(number):
    timeCounter = 0
    dt = 0.1
    accelList = []
    gyroList = []
    while timeCounter < number:
        accel = mpu.readAccelerometerMaster()
        gyro = mpu.readGyroscopeMaster()

        accelList.append(accel)
        gyroList.append(gyro)

        timeCounter += 1
        print(f"Plus que : {number + 1 -timeCounter} dixièmes de seconde pour le calcul du bruit !")
        time.sleep(dt)
    accel_x, accel_y, accel_z = [e[0] for e in accelList], [e[1] for e in accelList], [e[2] for e in accelList]
    accel_x_bias,accel_y_bias,accel_z_bias =  np.std(accel_x), np.std(accel_y), np.std(accel_z) 
    accel_x_noise,accel_y_noise,accel_z_noise =  np.mean(accel_x), np.mean(accel_y), np.mean(accel_z)

    gyro_z = [e[0] for e in gyroList], [e[1] for e in gyroList], [e[2] for e in gyroList]
    gyro_z_bias =  np.std(gyro_z) 
    gyro_z_noise =  np.mean(gyro_z)

    return accel_x_noise, accel_y_noise, accel_z_noise, gyro_z_noise, accel_x_bias, accel_y_bias, accel_z_bias, gyro_z_bias

### POUR LE KALMAN
def getData():
    accel = mpu.readAccelerometerMaster()
    gyro = mpu.readGyroscopeMaster()

    return accel + [gyro[2]]
