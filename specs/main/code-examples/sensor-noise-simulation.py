"""
Sensor Noise Simulation

Learning objective: Understand how physical sensors differ from ideal measurements due to noise
Estimated time: 10 minutes
Dependencies: numpy>=1.24.0, matplotlib>=3.7.0
"""

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt


def generate_ideal_signal(
    time_points: int = 100,
    frequency: float = 1.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate an ideal sinusoidal signal (perfect sensor reading).

    Args:
        time_points: Number of time points to generate
        frequency: Frequency of the sinusoidal signal in Hz

    Returns:
        Tuple of (time_array, signal_array)

    Example:
        >>> time, signal = generate_ideal_signal(100, 1.0)
        >>> len(signal)
        100
    """
    time = np.linspace(0, 4 * np.pi, time_points)
    ideal_signal = np.sin(frequency * time)
    return time, ideal_signal


def add_sensor_noise(
    signal: np.ndarray,
    noise_std: float = 0.1
) -> np.ndarray:
    """
    Add Gaussian noise to simulate real sensor measurements.

    Args:
        signal: The ideal signal array
        noise_std: Standard deviation of Gaussian noise (typical values: 0.05-0.2)

    Returns:
        Noisy signal array

    Example:
        >>> ideal = np.array([0, 1, 0, -1])
        >>> noisy = add_sensor_noise(ideal, noise_std=0.1)
        >>> noisy.shape == ideal.shape
        True
    """
    noise = np.random.normal(0, noise_std, size=signal.shape)
    noisy_signal = signal + noise
    return noisy_signal


def visualize_sensor_comparison(
    time: np.ndarray,
    ideal_signal: np.ndarray,
    noisy_signal: np.ndarray
) -> None:
    """
    Visualize the difference between ideal and noisy sensor readings.

    Args:
        time: Time array
        ideal_signal: Ideal sensor readings
        noisy_signal: Realistic noisy sensor readings
    """
    plt.figure(figsize=(10, 6))

    # Plot ideal signal
    plt.plot(time, ideal_signal, 'b-', linewidth=2, label='Ideal Sensor (No Noise)', alpha=0.7)

    # Plot noisy signal
    plt.plot(time, noisy_signal, 'r--', linewidth=1, label='Real Sensor (With Noise)', alpha=0.8)

    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Sensor Reading', fontsize=12)
    plt.title('Physical AI Challenge: Sensor Noise in Real Measurements', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def calculate_noise_metrics(
    ideal_signal: np.ndarray,
    noisy_signal: np.ndarray
) -> dict[str, float]:
    """
    Calculate statistical metrics to quantify sensor noise.

    Args:
        ideal_signal: The ideal signal
        noisy_signal: The noisy signal

    Returns:
        Dictionary containing RMSE, SNR, and max error
    """
    # Root Mean Square Error
    rmse = np.sqrt(np.mean((noisy_signal - ideal_signal) ** 2))

    # Signal-to-Noise Ratio (in dB)
    signal_power = np.mean(ideal_signal ** 2)
    noise_power = np.mean((noisy_signal - ideal_signal) ** 2)
    snr_db = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')

    # Maximum absolute error
    max_error = np.max(np.abs(noisy_signal - ideal_signal))

    return {
        'rmse': rmse,
        'snr_db': snr_db,
        'max_error': max_error
    }


def main():
    """Run the sensor noise simulation example."""
    print("=" * 60)
    print("SENSOR NOISE SIMULATION: Physical AI Challenge")
    print("=" * 60)
    print("\nSimulating sensor readings with realistic noise...\n")

    # Generate ideal signal
    time, ideal_signal = generate_ideal_signal(time_points=200, frequency=1.0)

    # Simulate real sensor with noise
    noisy_signal = add_sensor_noise(ideal_signal, noise_std=0.15)

    # Calculate metrics
    metrics = calculate_noise_metrics(ideal_signal, noisy_signal)

    print("Noise Metrics:")
    print(f"  • Root Mean Square Error (RMSE): {metrics['rmse']:.4f}")
    print(f"  • Signal-to-Noise Ratio (SNR): {metrics['snr_db']:.2f} dB")
    print(f"  • Maximum Absolute Error: {metrics['max_error']:.4f}")
    print("\n" + "=" * 60)
    print("KEY INSIGHT: Physical sensors always have noise!")
    print("This is why Physical AI must handle uncertainty.")
    print("=" * 60)

    # Visualize
    visualize_sensor_comparison(time, ideal_signal, noisy_signal)


if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    main()
