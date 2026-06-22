import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

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

def getInfo():
    timeCounter = 0

    accelList = []
    gyroList = []
    while timeCounter < 5:
        accel = mpu.readAccelerometerMaster()
        gyro = mpu.readGyroscopeMaster()

        accelList.append(accel)
        gyroList.append(gyro)

        timeCounter += 1
        time.sleep(1)
    print(accelList[:1])
    #accel_x_noise,accel_y_noise,accel_z_noise = accelList[:1]

getInfo()