from MPU6050 import *
import numpy as np
import getNoises as gn

###### DONNÉZS GLOBALES ######
dt = 0.1
isGivenNoises = 1 # pour recalculer le bruit du capteur immobile si 0
number = 60 #nombre d'échantillons qui seront utilisés pour le calcul des noises

if not isGivenNoises:
    accel_x_noise, accel_y_noise, accel_z_noise, gyro_z_noise = gn.getInfo(number)
else:
    accel_x_noise, accel_y_noise, accel_z_noise, gyro_z_noise = 0.01,0.01,0.01,0.01

class data:
    def __init__(self):
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0
        self.omega_z = 0

    def update(self):
        newdata = getData()
        self.a_x = newdata[0]
        self.a_y = newdata[1]
        self.a_z = newdata[2]-1
        self.omega_z = newdata[3]
    
    def getData(self):
        return np.array([self.a_x, self.a_y, self.a_z, self.omega_z])


class x_k:
    def __init__(self,x,y,z,v_x,v_y,v_z,a_x, a_y, a_z, theta_z, omega_z, biais):
        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z
        self.a_x = a_x
        self.a_y = a_y
        self.a_z = a_z
        self.theta_z = theta_z
        self.omega_z = omega_z
        self.biais = biais 

    def update(self,x,y,z,v_x,v_y,v_z,a_x, a_y, a_z, theta_z, omega_z, biais):
        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z
        self.a_x = a_x
        self.a_y = a_y
        self.a_z = a_z
        self.theta_z = theta_z
        self.omega_z = omega_z
        self.biais = biais 
    
    def getX(self):
        return np.array([self.x, self.y, self.z, self.v_x, self.v_y, self.v_z, self.a_x, self.a_y, self.a_z, self.theta_z, self.omega_z, self.biais])




class Kalman:
    def __init__(self):
        self.F = np.array([
            [1,0,0,dt,0,0,0,0,0,0,0,0],
            [0,1,0,0,dt,0,0,0,0,0,0,0],
            [0,0,1,0,0,dt,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,dt,-dt],
            [0,0,0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,1]
            ])
        
        self.data = data()
        self.B = np.array([[1/2*dt**2, 0, 0, 0],
                           [0,1/2*dt**2,0,0],
                           [0,0,1/2*dt**2,0],
                           [dt,0,0,0],
                           [0,dt,0,0],
                           [0,0,dt,0],
                           [1,0,0,0],
                           [0,1,0,0],
                           [0,0,1,0],
                           [0,0,0,dt],
                           [0,0,0,0],
                           [0,0,0,0]
                           ])
        self.x = x_k(0,0,0,0,0,0,0,0,0,0,0,0)
        self.P = np.eye(12)
        self.Q = np.diag([0.01,0.01,0.01,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.01, 0.01])
        self.R = np.diag([accel_x_noise,accel_y_noise,accel_z_noise, gyro_z_noise])
        self.H = np.array([
            [0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0]
            ])
        self.U = np.array([0,0,0,0])

    def updateU(self):
        self.data.update()
        self.U = self.data.getData()

    def x_estimation(self):
        x_prev = self.x.getX().reshape(12,1)
        self.updateU()
        return self.F @ x_prev + self.B @ self.U.reshape(4,1)
    
    def innovation(self):
        return self.data.getData().reshape(4,1) - self.H @ self.x_estimation()
    
    
    def P_estimation(self):
        return self.F @ self.P @ self.F.T + self.Q

    def S(self):
        return self.H @ self.P_estimation() @ self.H.T + self.R
    
    def K(self):
        return self.P_estimation() @ self.H.T @ np.linalg.inv(self.S())
    
    def update_turn(self):
        new_x = self.x_estimation() + self.K() @ self.innovation()
        new_x = new_x.flatten()
        I = np.eye(12)
        K = self.K()
        H= self.H
        P = self.P_estimation()
        R = self.R
        new_P = (I - K @ H) @ P @ (I - K @ H).T + K @ R @ K.T
        self.P = new_P
        self.x.update(new_x[0], new_x[1], new_x[2], new_x[3], new_x[4], new_x[5], new_x[6], new_x[7], new_x[8],new_x[9], new_x[10], new_x[11])


kal = Kalman()

accelList = []
theta_zList = []

for i in range(number):
    kal.data.update()
    kal.update_turn()
    x = kal.x.getX()
    accelList.append([x[6],x[7],x[8]])
    theta_zList.append(x[10])
    time.sleep(1)
print(accelList, theta_zList)





