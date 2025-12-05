"""
Multi-Sensor Fusion

Learning objective: Understand why robots combine multiple sensors for better perception
Estimated time: 12 minutes
Dependencies: numpy>=1.24.0, matplotlib>=3.7.0
"""

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt


def simulate_distance_measurement_camera(
    true_distance: float,
    num_samples: int = 100
) -> np.ndarray:
    """
    Simulate depth camera distance measurements (e.g., Intel RealSense).

    Args:
        true_distance: Ground truth distance in meters
        num_samples: Number of measurements

    Returns:
        Array of distance measurements

    Example:
        >>> distances = simulate_distance_measurement_camera(2.0, 50)
        >>> len(distances)
        50
    """
    # Depth cameras are accurate but have higher noise at longer ranges
    noise_std = 0.02 * true_distance  # 2% of distance
    measurements = np.random.normal(true_distance, noise_std, num_samples)

    # Occasionally miss detections (return NaN)
    miss_rate = 0.05  # 5% miss rate
    miss_mask = np.random.random(num_samples) < miss_rate
    measurements[miss_mask] = np.nan

    return measurements


def simulate_distance_measurement_lidar(
    true_distance: float,
    num_samples: int = 100
) -> np.ndarray:
    """
    Simulate LIDAR distance measurements (e.g., Velodyne VLP-16).

    Args:
        true_distance: Ground truth distance in meters
        num_samples: Number of measurements

    Returns:
        Array of distance measurements

    Example:
        >>> distances = simulate_distance_measurement_lidar(10.0, 50)
        >>> len(distances)
        50
    """
    # LIDAR has consistent accuracy across distances (±3cm)
    noise_std = 0.03  # 3cm standard deviation
    measurements = np.random.normal(true_distance, noise_std, num_samples)

    # Very rarely misses (more reliable than cameras)
    miss_rate = 0.01  # 1% miss rate
    miss_mask = np.random.random(num_samples) < miss_rate
    measurements[miss_mask] = np.nan

    return measurements


def weighted_fusion(
    camera_meas: np.ndarray,
    lidar_meas: np.ndarray,
    camera_weight: float = 0.4,
    lidar_weight: float = 0.6
) -> np.ndarray:
    """
    Fuse camera and LIDAR measurements using weighted average.

    Args:
        camera_meas: Camera distance measurements
        lidar_meas: LIDAR distance measurements
        camera_weight: Weight for camera (0-1)
        lidar_weight: Weight for LIDAR (0-1)

    Returns:
        Fused distance estimates

    Example:
        >>> cam = np.array([2.1, 2.0, np.nan])
        >>> lid = np.array([2.05, 2.03, 2.02])
        >>> fused = weighted_fusion(cam, lid, 0.5, 0.5)
        >>> len(fused)
        3
    """
    fused = np.zeros(len(camera_meas))

    for i in range(len(camera_meas)):
        cam_val = camera_meas[i]
        lid_val = lidar_meas[i]

        # Handle missing measurements
        if np.isnan(cam_val) and np.isnan(lid_val):
            fused[i] = np.nan  # Both sensors failed
        elif np.isnan(cam_val):
            fused[i] = lid_val  # Use only LIDAR
        elif np.isnan(lid_val):
            fused[i] = cam_val  # Use only camera
        else:
            # Both available: weighted fusion
            fused[i] = camera_weight * cam_val + lidar_weight * lid_val

    return fused


def calculate_sensor_metrics(
    measurements: np.ndarray,
    true_value: float
) -> dict[str, float]:
    """
    Calculate accuracy metrics for sensor measurements.

    Args:
        measurements: Sensor measurements (may contain NaN)
        true_value: Ground truth value

    Returns:
        Dictionary with RMSE, bias, and miss rate
    """
    valid_meas = measurements[~np.isnan(measurements)]

    if len(valid_meas) == 0:
        return {'rmse': float('inf'), 'bias': float('inf'), 'miss_rate': 1.0}

    errors = valid_meas - true_value
    rmse = np.sqrt(np.mean(errors ** 2))
    bias = np.mean(errors)
    miss_rate = np.sum(np.isnan(measurements)) / len(measurements)

    return {
        'rmse': rmse,
        'bias': bias,
        'miss_rate': miss_rate
    }


def visualize_sensor_fusion(
    camera_meas: np.ndarray,
    lidar_meas: np.ndarray,
    fused_meas: np.ndarray,
    true_distance: float
) -> None:
    """
    Visualize the sensor fusion results.

    Args:
        camera_meas: Camera measurements
        lidar_meas: LIDAR measurements
        fused_meas: Fused measurements
        true_distance: Ground truth
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    samples = np.arange(len(camera_meas))

    # Plot individual sensor measurements
    ax1.scatter(samples, camera_meas, alpha=0.5, s=30, label='Camera', color='blue', marker='o')
    ax1.scatter(samples, lidar_meas, alpha=0.5, s=30, label='LIDAR', color='red', marker='s')
    ax1.axhline(true_distance, color='green', linestyle='--', linewidth=2, label='True Distance', alpha=0.7)
    ax1.set_ylabel('Distance (meters)', fontsize=11)
    ax1.set_title('Individual Sensor Measurements', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim([-2, len(samples)])

    # Plot fused measurements
    ax2.scatter(samples, fused_meas, alpha=0.6, s=30, label='Fused Estimate', color='purple', marker='^')
    ax2.axhline(true_distance, color='green', linestyle='--', linewidth=2, label='True Distance', alpha=0.7)

    # Show confidence band
    valid_fused = fused_meas[~np.isnan(fused_meas)]
    if len(valid_fused) > 0:
        std_fused = np.std(valid_fused)
        ax2.fill_between(samples, true_distance - std_fused, true_distance + std_fused,
                         alpha=0.2, color='purple', label='±1 Std Dev')

    ax2.set_xlabel('Sample Number', fontsize=11)
    ax2.set_ylabel('Distance (meters)', fontsize=11)
    ax2.set_title('Fused Sensor Estimate (More Accurate!)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([-2, len(samples)])

    plt.suptitle('Multi-Sensor Fusion: Better Together', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def main():
    """Run the multi-sensor fusion example."""
    print("=" * 60)
    print("MULTI-SENSOR FUSION: Why Robots Use Multiple Sensors")
    print("=" * 60)
    print("\nScenario: Robot measuring distance to an obstacle\n")

    # Ground truth
    true_distance = 3.5  # meters
    num_samples = 100

    print(f"True distance: {true_distance:.2f} meters\n")

    # Simulate sensors
    camera_measurements = simulate_distance_measurement_camera(true_distance, num_samples)
    lidar_measurements = simulate_distance_measurement_lidar(true_distance, num_samples)

    # Fuse measurements
    fused_measurements = weighted_fusion(camera_measurements, lidar_measurements,
                                        camera_weight=0.4, lidar_weight=0.6)

    # Calculate metrics
    camera_metrics = calculate_sensor_metrics(camera_measurements, true_distance)
    lidar_metrics = calculate_sensor_metrics(lidar_measurements, true_distance)
    fused_metrics = calculate_sensor_metrics(fused_measurements, true_distance)

    print("Performance Comparison:")
    print(f"\n  Camera (Intel RealSense D455):")
    print(f"    • RMSE: {camera_metrics['rmse']:.4f} m")
    print(f"    • Bias: {camera_metrics['bias']:.4f} m")
    print(f"    • Miss Rate: {camera_metrics['miss_rate']*100:.1f}%")

    print(f"\n  LIDAR (Velodyne VLP-16):")
    print(f"    • RMSE: {lidar_metrics['rmse']:.4f} m")
    print(f"    • Bias: {lidar_metrics['bias']:.4f} m")
    print(f"    • Miss Rate: {lidar_metrics['miss_rate']*100:.1f}%")

    print(f"\n  Fused Estimate (Weighted Fusion):")
    print(f"    • RMSE: {fused_metrics['rmse']:.4f} m")
    print(f"    • Bias: {fused_metrics['bias']:.4f} m")
    print(f"    • Miss Rate: {fused_metrics['miss_rate']*100:.1f}%")

    # Calculate improvement
    improvement = ((camera_metrics['rmse'] - fused_metrics['rmse']) / camera_metrics['rmse']) * 100

    print("\n" + "=" * 60)
    print(f"KEY INSIGHT: Fusion improves accuracy by {improvement:.1f}%")
    print("Each sensor has different strengths and weaknesses.")
    print("Combining them produces more robust perception!")
    print("=" * 60)

    # Visualize
    visualize_sensor_fusion(camera_measurements, lidar_measurements, fused_measurements, true_distance)


if __name__ == "__main__":
    np.random.seed(42)
    main()
