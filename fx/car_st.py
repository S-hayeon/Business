import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
L = 2.5  # Wheelbase (m)
max_steering_angle = 30  # Maximum steering lock in degrees

# Function to calculate slip angle
def calculate_slip_angle(v, beta, delta):
    return np.arctan((v * np.sin(beta)) / (v * np.cos(beta) + L * np.sin(delta)))

# Function to plot the car icon
def plot_car_icon(x, y, heading):
    car_length = L
    car_width = 1.5

    x_corners = [x, x + car_length * np.cos(heading), x + car_length * np.cos(heading) + car_width * np.sin(heading)]
    y_corners = [y, y + car_length * np.sin(heading), y - car_width * np.cos(heading)]

    plt.fill(x_corners, y_corners, "b")
    plt.plot(x_corners + [x_corners[0]], y_corners + [y_corners[0]], "k")

# Streamlit app
def main():
    st.title("Slip Angle Simulation")

    # Input sliders
    v = st.slider("Vehicle Speed (m/s)", min_value=5, max_value=30, value=10, step=1)
    beta = st.slider("Yaw Angle (degrees)", min_value=-30, max_value=30, value=0, step=1)
    delta = st.slider(
        "Steering Angle (degrees)", min_value=-max_steering_angle, max_value=max_steering_angle, value=0, step=1
    )

    # Calculate slip angle
    slip_angle = calculate_slip_angle(np.radians(v), np.radians(beta), np.radians(delta))

    # Display slip angle
    st.write(f"Slip Angle: {np.degrees(slip_angle):.2f} degrees")

    # Plot the car's trajectory with car icon
    fig=plt.figure(figsize=(8, 6))
    plt.plot([0, L * np.cos(np.radians(beta))], [0, L * np.sin(np.radians(beta))], "r-", label="Car's Trajectory")
    plot_car_icon(L * np.cos(np.radians(beta)), L * np.sin(np.radians(beta)), np.radians(beta))
    plt.xlim(-L, L)
    plt.ylim(0, L)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend()
    plt.title("Car's Trajectory on the Race Track")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
