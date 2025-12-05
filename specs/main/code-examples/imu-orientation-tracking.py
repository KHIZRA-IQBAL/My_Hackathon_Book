"""
IMU Orientation Tracking

Learning objective: Understand IMU drift and the challenges of integration-based tracking
Estimated time: 12 minutes
Dependencies: numpy>=1.24.0, matplotlib>=3.7.0
"""

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt


def simulate_angular_velocity(
    time: np.ndarray,
    true_rotation_rate: float = 0.5
) -> np.ndarray:
    """
    Simulate gyroscope measurements (angular velocity in rad/s).

    Args:
        time: Time array in seconds
        true_rotation_rate: True angular velocity in rad/s

    Returns:
        Array of angular velocity measurements

    Example:
        >>> time = np.linspace(0, 10, 100)
        >>> omega = simulate_angular_velocity(time, 0.5)
        >>> len(omega)
        100
    """
    # True angular velocity (constant rotation)
    omega_true = np.full_like(time, true_rotation_rate)

    # Add measurement noise (Bosch BMI088: noise density ~0.014 rad/s/√Hz)
    noise = np.random.normal(0, 0.02, size=omega_true.shape)

    # Add bias drift (gyroscope bias changes slowly over time)
    drift = 0.01 * np.sin(0.1 * time)  # Slow sinusoidal drift

    omega_measured = omega_true + noise + drift

    return omega_measured


def integrate_orientation(
    omega: np.ndarray,
    dt: float,
    initial_angle: float = 0.0
) -> np.ndarray:
    """
    Integrate angular velocity to get orientation (Euler integration).

    Args:
        omega: Angular velocity measurements in rad/s
        dt: Time step in seconds
        initial_angle: Starting orientation in radians

    Returns:
        Array of orientation angles in radians

    Example:
        >>> omega = np.array([1.0, 1.0, 1.0])
        >>> angles = integrate_orientation(omega, dt=0.1, initial_angle=0)
        >>> len(angles)
        3
    """
    angles = np.zeros(len(omega))
    angles[0] = initial_angle

    for i in range(1, len(omega)):
        # Euler integration: θ(t+dt) = θ(t) + ω(t) * dt
        angles[i] = angles[i-1] + omega[i-1] * dt

    return angles


def calculate_true_orientation(time: np.ndarray, rotation_rate: float) -> np.ndarray:
    """
    Calculate ground truth orientation for comparison.

    Args:
        time: Time array
        rotation_rate: True angular velocity

    Returns:
        True orientation angles
    """
    return rotation_rate * time


def visualize_imu_drift(
    time: np.ndarray,
    true_angles: np.ndarray,
    measured_angles: np.ndarray
) -> None:
    """
    Visualize the IMU drift problem.

    Args:
        time: Time array in seconds
        true_angles: Ground truth orientation
        measured_angles: IMU-based orientation estimate
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot orientation comparison
    ax1.plot(time, np.rad2deg(true_angles), 'g-', linewidth=2, label='True Orientation', alpha=0.7)
    ax1.plot(time, np.rad2deg(measured_angles), 'r--', linewidth=1.5, label='IMU Estimate', alpha=0.8)
    ax1.set_xlabel('Time (seconds)', fontsize=11)
    ax1.set_ylabel('Orientation (degrees)', fontsize=11)
    ax1.set_title('IMU Orientation Tracking: The Drift Problem', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Plot error accumulation
    error = np.abs(measured_angles - true_angles)
    ax2.plot(time, np.rad2deg(error), 'b-', linewidth=2, label='Absolute Error')
    ax2.fill_between(time, 0, np.rad2deg(error), alpha=0.3)
    ax2.set_xlabel('Time (seconds)', fontsize=11)
    ax2.set_ylabel('Error (degrees)', fontsize=11)
    ax2.set_title('Error Accumulation Over Time', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def calculate_drift_metrics(
    true_angles: np.ndarray,
    measured_angles: np.ndarray,
    time: np.ndarray
) -> dict[str, float]:
    """
    Calculate metrics to quantify IMU drift.

    Args:
        true_angles: Ground truth
        measured_angles: IMU estimates
        time: Time array

    Returns:
        Dictionary with drift metrics
    """
    error = measured_angles - true_angles

    return {
        'final_error_deg': np.rad2deg(abs(error[-1])),
        'mean_error_deg': np.rad2deg(np.mean(np.abs(error))),
        'drift_rate_deg_per_sec': np.rad2deg(abs(error[-1])) / time[-1]
    }


def main():
    """Run the IMU orientation tracking example."""
    print("=" * 60)
    print("IMU ORIENTATION TRACKING: The Drift Problem")
    print("=" * 60)
    print("\nSimulating Bosch BMI088 IMU (used in humanoid robots)...\n")

    # Simulation parameters
    duration = 30.0  # seconds
    dt = 0.01  # 100 Hz sampling rate (typical for IMU)
    time = np.arange(0, duration, dt)
    rotation_rate = 0.5  # rad/s (constant rotation)

    # Simulate gyroscope measurements
    omega_measured = simulate_angular_velocity(time, rotation_rate)

    # Integrate to get orientation
    measured_angles = integrate_orientation(omega_measured, dt)
    true_angles = calculate_true_orientation(time, rotation_rate)

    # Calculate drift metrics
    metrics = calculate_drift_metrics(true_angles, measured_angles, time)

    print("Drift Metrics (after 30 seconds):")
    print(f"  • Final Error: {metrics['final_error_deg']:.2f}°")
    print(f"  • Mean Absolute Error: {metrics['mean_error_deg']:.2f}°")
    print(f"  • Drift Rate: {metrics['drift_rate_deg_per_sec']:.3f}°/second")
    print("\n" + "=" * 60)
    print("KEY INSIGHT: Integration causes error accumulation!")
    print("Solution: Sensor fusion (combine IMU with cameras/GPS)")
    print("=" * 60)

    # Visualize
    visualize_imu_drift(time, true_angles, measured_angles)


if __name__ == "__main__":
    np.random.seed(42)
    main()
