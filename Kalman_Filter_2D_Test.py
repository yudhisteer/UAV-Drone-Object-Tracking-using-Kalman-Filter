from Kalman_Filter_Custom_2D import KalmanFilter

import numpy as np
import matplotlib.pyplot as plt
import math

# Generate synthetic measurements
np.random.seed(0)
num_measurements = 50

# Car parameters
initial_position = np.array([0, 0])
speed = 5.0  # m/s
heading = 45.0  # degrees

# Convert heading to radians
heading_rad = math.radians(heading)

# Calculate true positions based on constant speed and heading
true_positions = [initial_position]
for _ in range(num_measurements-1):
    delta_x = speed * math.cos(heading_rad)
    delta_y = speed * math.sin(heading_rad)
    new_position = true_positions[-1] + np.array([delta_x, delta_y])
    true_positions.append(new_position)
true_positions = np.array(true_positions).T

# Add noise to simulate measurement errors
measurement_noise_std = 5
measurements = true_positions + np.random.normal(0, measurement_noise_std, size=true_positions.shape)

# Kalman filter parameters
dt = 1.0  # Sampling time
INIT_POS_STD = 10  # Initial position standard deviation
INIT_VEL_STD = 10  # Initial velocity standard deviation
ACCEL_STD = .1  # Acceleration standard deviation
GPS_POS_STD = 5  # Measurement position standard deviation

# Kalman filter initialization
kf = KalmanFilter(dt, INIT_POS_STD, INIT_VEL_STD, ACCEL_STD, GPS_POS_STD)

# Lists to store filtered states
filtered_states = []

# Perform prediction and update steps for each measurement
for measurement in measurements.T:
    # Prediction step
    predicted_state = kf.predict()

    # Update step
    updated_state = kf.update(measurement)

    # Store the filtered state
    filtered_states.append(updated_state)

# Convert filtered states to numpy array
filtered_states = np.array(filtered_states).T

# Plot the results
plt.figure()
plt.plot(true_positions[0], true_positions[1], color='red', label='True Position')
plt.scatter(measurements[0], measurements[1], marker='x', label='Measurements')
plt.scatter(filtered_states[0], filtered_states[1], color='green', label='Filtered Position')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Kalman Filter - Car Tracking')
plt.legend()
plt.grid(True)
plt.savefig('plot.png')  # Save the plot as a PNG image
plt.show()

