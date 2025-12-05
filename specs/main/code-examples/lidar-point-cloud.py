"""
LIDAR Point Cloud Visualization

Learning objective: Understand LIDAR sensor output as 3D point clouds
Estimated time: 12 minutes
Dependencies: numpy>=1.24.0, matplotlib>=3.7.0
"""

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def simulate_lidar_scan(
    num_points: int = 1000,
    max_range: float = 10.0,
    vertical_fov: Tuple[float, float] = (-15, 15)
) -> np.ndarray:
    """
    Simulate a LIDAR scan of a simple environment (walls and objects).

    Args:
        num_points: Number of LIDAR points to generate
        max_range: Maximum detection range in meters (e.g., Velodyne VLP-16: 100m)
        vertical_fov: Vertical field of view in degrees (min, max)

    Returns:
        Array of shape (num_points, 3) containing [x, y, z] coordinates

    Example:
        >>> points = simulate_lidar_scan(100, 10.0)
        >>> points.shape
        (100, 3)
    """
    points = []

    # Simulate walls (rectangular room)
    for _ in range(num_points // 2):
        # Random azimuth angle (0-360 degrees)
        azimuth = np.random.uniform(0, 2 * np.pi)

        # Random vertical angle within FOV
        elevation = np.deg2rad(np.random.uniform(vertical_fov[0], vertical_fov[1]))

        # Distance to wall (simulate rectangular room)
        if np.cos(azimuth) > 0:
            distance = min(5.0 / abs(np.cos(azimuth)), max_range)
        else:
            distance = min(5.0 / abs(np.cos(azimuth)) if np.cos(azimuth) != 0 else max_range, max_range)

        # Convert spherical to Cartesian coordinates
        x = distance * np.cos(elevation) * np.cos(azimuth)
        y = distance * np.cos(elevation) * np.sin(azimuth)
        z = distance * np.sin(elevation)

        points.append([x, y, z])

    # Simulate obstacles (boxes in the room)
    for _ in range(num_points // 2):
        # Object at position (2, 2, 0) with size 1x1x1 meters
        x = np.random.uniform(1.5, 2.5)
        y = np.random.uniform(1.5, 2.5)
        z = np.random.uniform(-0.5, 0.5)
        points.append([x, y, z])

    return np.array(points)


def add_lidar_noise(
    points: np.ndarray,
    range_accuracy: float = 0.03
) -> np.ndarray:
    """
    Add realistic noise to LIDAR measurements.

    Args:
        points: Clean point cloud array
        range_accuracy: Range measurement accuracy in meters (Velodyne VLP-16: ±3cm)

    Returns:
        Noisy point cloud array
    """
    noise = np.random.normal(0, range_accuracy, size=points.shape)
    noisy_points = points + noise
    return noisy_points


def visualize_point_cloud(
    points: np.ndarray,
    title: str = "LIDAR Point Cloud"
) -> None:
    """
    Visualize 3D point cloud from LIDAR scan.

    Args:
        points: Array of shape (N, 3) with xyz coordinates
        title: Plot title
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Color points by height (z-coordinate)
    colors = points[:, 2]

    scatter = ax.scatter(
        points[:, 0],
        points[:, 1],
        points[:, 2],
        c=colors,
        cmap='viridis',
        s=2,
        alpha=0.6
    )

    ax.set_xlabel('X (meters)', fontsize=11)
    ax.set_ylabel('Y (meters)', fontsize=11)
    ax.set_zlabel('Z (meters)', fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
    cbar.set_label('Height (m)', fontsize=10)

    # Set equal aspect ratio for better visualization
    max_range = np.abs(points).max()
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range/2, max_range/2])

    plt.tight_layout()
    plt.show()


def calculate_point_cloud_stats(points: np.ndarray) -> dict[str, float]:
    """
    Calculate statistics about the point cloud.

    Args:
        points: Point cloud array

    Returns:
        Dictionary with statistics
    """
    return {
        'num_points': len(points),
        'mean_distance': np.mean(np.linalg.norm(points, axis=1)),
        'max_distance': np.max(np.linalg.norm(points, axis=1)),
        'height_range': np.ptp(points[:, 2]),  # Peak-to-peak in z
        'density': len(points) / (np.ptp(points[:, 0]) * np.ptp(points[:, 1]))
    }


def main():
    """Run the LIDAR point cloud visualization example."""
    print("=" * 60)
    print("LIDAR POINT CLOUD VISUALIZATION")
    print("=" * 60)
    print("\nSimulating Velodyne VLP-16 LIDAR scan...\n")

    # Simulate LIDAR scan
    points = simulate_lidar_scan(num_points=2000, max_range=10.0)

    # Add realistic noise
    noisy_points = add_lidar_noise(points, range_accuracy=0.03)

    # Calculate statistics
    stats = calculate_point_cloud_stats(noisy_points)

    print("Point Cloud Statistics:")
    print(f"  • Total Points: {stats['num_points']:.0f}")
    print(f"  • Mean Distance: {stats['mean_distance']:.2f} m")
    print(f"  • Max Distance: {stats['max_distance']:.2f} m")
    print(f"  • Height Range: {stats['height_range']:.2f} m")
    print(f"  • Point Density: {stats['density']:.1f} points/m²")
    print("\n" + "=" * 60)
    print("KEY INSIGHT: LIDAR provides sparse 3D structure")
    print("Robots must process ~300,000 points/second in real-time!")
    print("=" * 60)

    # Visualize
    visualize_point_cloud(noisy_points, "LIDAR Scan: Simulated Room with Obstacle")


if __name__ == "__main__":
    np.random.seed(42)
    main()
