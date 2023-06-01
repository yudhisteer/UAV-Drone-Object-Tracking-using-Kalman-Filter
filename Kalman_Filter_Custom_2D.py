import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

class KalmanFilter(object):
    def __init__(self, dt, INIT_POS_STD, INIT_VEL_STD, ACCEL_STD, GPS_POS_STD):

        """
        :param dt: sampling time (time for 1 cycle)
        :param INIT_POS_STD: initial position standard deviation in x-direction
        :param INIT_VEL_STD: initial position standard deviation in y-direction
        :param ACCEL_STD: process noise magnitude
        :param GPS_POS_STD: standard deviation of the measurement
        """

        # Define sampling time
        self.dt = dt

        # Intial State
        self.x = np.zeros((4, 1))

        # State Estimate Covariance Matrix
        cov = np.zeros((4, 4))
        cov[0, 0] = INIT_POS_STD ** 2
        cov[1, 1] = INIT_POS_STD ** 2
        cov[2, 2] = INIT_VEL_STD ** 2
        cov[3, 3] = INIT_VEL_STD ** 2
        self.P = cov

        # State Transition Matrix
        self.F = np.array([[1, 0, self.dt, 0],
                           [0, 1, 0, self.dt],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

        # Covariance of Process model noise
        q = np.zeros((2, 2))
        q[0, 0] = ACCEL_STD ** 2
        q[1, 1] = ACCEL_STD ** 2
        self.q = q

        # Process Model Sensitivity Matrix
        L = np.zeros((4, 2))
        L[0, 0] = 0.5 * self.dt ** 2
        L[1, 1] = 0.5 * self.dt ** 2
        L[2, 0] = self.dt
        L[3, 1] = self.dt
        self.L = L

        # Process model noise
        self.Q = np.dot(self.L, np.dot(self.q, (self.L).T))

        # Define Measurement Mapping Matrix
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])

        # Measurement Covariance Matrix
        R = np.zeros((2, 2))
        R[0, 0] = GPS_POS_STD ** 2
        R[1, 1] = GPS_POS_STD ** 2
        self.R = R

    # PREDICTION STEP
    def predict(self):
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(self.F, np.dot(self.P, (self.F).T)) + self.Q

        x_pred = self.x[0]
        y_pred = self.x[1]
        return x_pred, y_pred

    # UPDATE STEP
    def update(self, z):
        # Innovation
        z_hat = np.dot(self.H, self.x)
        self.y = z - z_hat

        # Innovation Covariance
        self.S = np.dot(self.H, np.dot(self.P, (self.H).T)) + self.R

        # Kalman Gain
        self.K = np.dot(self.P, np.dot((self.H).T, np.linalg.inv(self.S)))

        I = np.eye(4)

        self.x = self.x + np.dot(self.K, self.y)
        self.P = np.dot((I - np.dot(self.K, self.H)), self.P)

        x_updated = self.x[0]
        y_updated = self.x[1]
        return x_updated, y_updated




