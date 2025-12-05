"""
Camera Image Processing

Learning objective: Understand basic computer vision operations for robotics
Estimated time: 10 minutes
Dependencies: numpy>=1.24.0, matplotlib>=3.7.0, pillow>=9.0.0
"""

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter


def create_synthetic_scene() -> np.ndarray:
    """
    Create a synthetic robot vision scene (simulated camera image).

    Returns:
        RGB image as numpy array of shape (H, W, 3)

    Example:
        >>> img = create_synthetic_scene()
        >>> img.shape[2]  # RGB channels
        3
    """
    # Create a simple scene with shapes (representing objects)
    width, height = 640, 480
    image = np.ones((height, width, 3), dtype=np.uint8) * 200  # Gray background

    # Add a "table" (brown rectangle)
    image[300:450, 100:540] = [139, 90, 43]  # Brown color

    # Add objects on the table
    # Object 1: Red cube (top-left)
    image[250:300, 150:200] = [220, 50, 50]

    # Object 2: Blue cylinder (top-right)
    image[260:310, 400:450] = [50, 50, 220]

    # Object 3: Green sphere (center)
    center_y, center_x = 280, 320
    radius = 30
    y, x = np.ogrid[:height, :width]
    mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2
    image[mask] = [50, 220, 50]

    return image


def rgb_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert RGB image to grayscale using luminosity method.

    Args:
        image: RGB image array of shape (H, W, 3)

    Returns:
        Grayscale image array of shape (H, W)

    Example:
        >>> rgb = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        >>> gray = rgb_to_grayscale(rgb)
        >>> gray.shape
        (100, 100)
    """
    # Luminosity method: 0.299*R + 0.587*G + 0.114*B
    grayscale = (
        0.299 * image[:, :, 0] +
        0.587 * image[:, :, 1] +
        0.114 * image[:, :, 2]
    ).astype(np.uint8)

    return grayscale


def simple_edge_detection(image: np.ndarray, threshold: int = 30) -> np.ndarray:
    """
    Detect edges using simple gradient-based method (Sobel-like).

    Args:
        image: Grayscale image array
        threshold: Edge strength threshold (0-255)

    Returns:
        Binary edge map
    """
    # Convert to PIL Image for filtering
    pil_img = Image.fromarray(image)

    # Apply edge detection filter
    edges_pil = pil_img.filter(ImageFilter.FIND_EDGES)
    edges = np.array(edges_pil)

    # Threshold to create binary edge map
    binary_edges = (edges > threshold).astype(np.uint8) * 255

    return binary_edges


def apply_blur(image: np.ndarray, radius: int = 2) -> np.ndarray:
    """
    Apply Gaussian blur to reduce noise (common preprocessing step).

    Args:
        image: Input image array
        radius: Blur radius (larger = more blur)

    Returns:
        Blurred image array
    """
    pil_img = Image.fromarray(image)
    blurred_pil = pil_img.filter(ImageFilter.GaussianBlur(radius=radius))
    return np.array(blurred_pil)


def visualize_processing_pipeline(
    original: np.ndarray,
    grayscale: np.ndarray,
    edges: np.ndarray
) -> None:
    """
    Visualize the image processing pipeline.

    Args:
        original: Original RGB image
        grayscale: Grayscale version
        edges: Edge detection result
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Original image
    axes[0].imshow(original)
    axes[0].set_title('Original Camera Image\n(RGB from Intel RealSense)', fontsize=12, fontweight='bold')
    axes[0].axis('off')

    # Grayscale
    axes[1].imshow(grayscale, cmap='gray')
    axes[1].set_title('Grayscale Conversion\n(First preprocessing step)', fontsize=12, fontweight='bold')
    axes[1].axis('off')

    # Edge detection
    axes[2].imshow(edges, cmap='gray')
    axes[2].set_title('Edge Detection\n(Object boundaries)', fontsize=12, fontweight='bold')
    axes[2].axis('off')

    plt.suptitle('Camera Image Processing Pipeline for Robot Vision', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


def calculate_processing_stats(edges: np.ndarray) -> dict[str, float]:
    """
    Calculate statistics from processed image.

    Args:
        edges: Binary edge map

    Returns:
        Dictionary with statistics
    """
    edge_pixels = np.sum(edges > 0)
    total_pixels = edges.size

    return {
        'edge_pixels': edge_pixels,
        'edge_percentage': 100.0 * edge_pixels / total_pixels,
        'total_pixels': total_pixels
    }


def main():
    """Run the camera image processing example."""
    print("=" * 60)
    print("CAMERA IMAGE PROCESSING: Robot Vision Basics")
    print("=" * 60)
    print("\nSimulating Intel RealSense D455 camera processing...\n")

    # Create synthetic scene
    original_image = create_synthetic_scene()

    # Processing pipeline
    print("Processing steps:")
    print("  1. Capture RGB image (640x480)")
    print("  2. Convert to grayscale (reduce data)")
    print("  3. Apply edge detection (find objects)")

    # Convert to grayscale
    grayscale = rgb_to_grayscale(original_image)

    # Apply slight blur to reduce noise
    grayscale_blurred = apply_blur(grayscale, radius=1)

    # Detect edges
    edges = simple_edge_detection(grayscale_blurred, threshold=20)

    # Calculate statistics
    stats = calculate_processing_stats(edges)

    print(f"\nProcessing Results:")
    print(f"  • Image Resolution: {original_image.shape[1]}x{original_image.shape[0]}")
    print(f"  • Total Pixels: {stats['total_pixels']:,}")
    print(f"  • Edge Pixels Detected: {stats['edge_pixels']:,}")
    print(f"  • Edge Density: {stats['edge_percentage']:.2f}%")
    print("\n" + "=" * 60)
    print("KEY INSIGHT: Robots process images at 30-60 FPS")
    print("Must be fast and efficient for real-time control!")
    print("=" * 60)

    # Visualize
    visualize_processing_pipeline(original_image, grayscale, edges)


if __name__ == "__main__":
    main()
