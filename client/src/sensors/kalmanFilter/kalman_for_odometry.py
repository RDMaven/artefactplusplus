import numpy as np
import src.sensors.kalmanFilter.getNoises as gn
import time

###### DONNÉES GLOBALES ######
dt = 0.1
isGivenNoises = 1 # pour recalculer le bruit du capteur immobile si 0
noiseNumber = 250 #Nombre de données pour l'initialisation

if not isGivenNoises:
    accel_x_noise, accel_y_noise, accel_z_noise, gyro_z_noise,accel_x_bias, accel_y_bias, accel_z_bias, gyro_z_bias = gn.getInfo(noiseNumber)
else:
    ### A initialiser pour un grand number
    accel_x_noise= 0.001944567418940276
    accel_y_noise=0.0019362013371498731
    accel_z_noise=0.0032176589968624272
    gyro_z_noise=0.12445350857045176
    accel_x_bias = 0.018384033203125
    accel_y_bias = 0.0015986328125
    accel_z_bias=1.16818017578125
    gyro_z_bias =1.499359130859375

###### CLASSES ######

class data:
    def __init__(self):
        self.a_x = 0
        self.a_y = 0
        self.a_z = 0
        self.omega_z = 0

    def update(self):
        newdata = gn.getData()
        self.a_x = newdata[0]-accel_x_bias
        self.a_y = newdata[1]-accel_y_bias
        self.a_z = newdata[2]-accel_z_bias
        self.omega_z = newdata[3] - gyro_z_bias
    
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
            [1,0,0,dt,0,0,1/2*dt**2,0,0,0,0,0],
            [0,1,0,0,dt,0,0,1/2*dt**2,0,0,0,0],
            [0,0,1,0,0,dt,0,0,1/2*dt**2,0,0,0],
            [0,0,0,1,0,0,dt,0,0,0,0,0],
            [0,0,0,0,1,0,0,dt,0,0,0,0],
            [0,0,0,0,0,1,0,0,dt,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,dt,-dt],
            [0,0,0,0,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,1]
            ])
        
        self.data = data()
        self.B = np.array([[0],[0],[0],[0],[0],[0],[0],[0],[0],[dt],[0],[0]])
        self.x = x_k(0,0,0,0,0,0,0,0,0,0,0,0)
        self.P = np.eye(12)
        self.Q = np.diag([
                1e-6, 1e-6, 1e-6, # x, y, z (positions)
                5e-4, 5e-4, 5e-4, # vx, vy, vz (vitesses)
                1e-7, 1e-7, 1e-7, # ax, ay, az (accélérations) <-- Divisé par 10 (anciennement 1e-6)
                1e-5,             # theta_z
                1e-5,             # omega_z       <-- Divisé par 10 (anciennement 1e-4)
                1e-6              # biais
            ])
        self.R = np.diag([accel_x_noise**2,accel_y_noise**2,accel_z_noise**2, gyro_z_noise**2])
        self.H = np.array([
            [0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0]
            ])
        self.U = np.array([[self.data.omega_z]])

    def updateU(self,da):
        self.data.update()
        self.U = np.array([[da[3]]])

    def x_estimation(self,da):
        x_prev = self.x.getX().reshape(12,1)
        self.updateU(da)
        return self.F @ x_prev + self.B @ self.U
    
    def innovation(self, x_est,da):
        return da.reshape(4,1) - self.H @ x_est
    
    
    def P_estimation(self):
        return self.F @ self.P @ self.F.T + self.Q

    def S(self, P):
        return self.H @ P @ self.H.T + self.R
    
    def K(self, P, S):
        return P @ self.H.T @ np.linalg.inv(S)
    
    def update_turn(self,da):
        I = np.eye(12)
        P = self.P_estimation()
        x_est = self.x_estimation(da)
        innov = self.innovation(x_est,da)
        S = self.S(P)
        K = self.K(P,S)
        H= self.H
        R = self.R
        new_x = x_est + K @ innov
        new_x = new_x.flatten()
        
        new_P = (I - K @ H) @ P @ (I - K @ H).T + K @ R @ K.T
        self.P = new_P
        self.x.update(new_x[0], new_x[1], new_x[2], new_x[3], new_x[4], new_x[5], new_x[6], new_x[7], new_x[8],new_x[9], new_x[10], new_x[11])
    
    def __str__(self):
        x = self.x.getX()
        return f"Kalman position : x={x[0]}, y={x[1]}, theta={x[9]}°"

    def kalman_one_turn(self):
        self.data.update()
        da = self.data.getData()
        self.update_turn(da)
