# Sensor Systems for Physical AI - Content Outline

## Front Matter
```yaml
---
sidebar_position: 5
title: "Sensor Systems for Physical AI"
description: "Deep dive into LIDAR, cameras, IMUs, force/torque sensors and multi-sensor fusion"
---
```

## Learning Objectives (FR-024)
1. Explain how LIDAR sensors create 3D point clouds
2. Understand depth cameras vs. RGB cameras and their trade-offs
3. Describe IMU drift and why integration causes error accumulation
4. Recognize when to use force/torque sensors for manipulation
5. Understand why multi-sensor fusion produces better estimates than single sensors
6. Implement basic sensor processing and fusion in Python

## Prerequisites (FR-025)
- Completed: Previous 4 pages
- Python with numpy, matplotlib
- Estimated time: 50 minutes (includes running code examples)

## Content Structure

### Section 1: Introduction to Robot Perception (300 words)
**Embed**: Sensor Data Flow Mermaid diagram

**Key concepts**:
- Sensor layer → Processing layer → Decision layer
- Multiple sensor types compensate for individual weaknesses
- Real-time requirements

**Content outline**:
- Physical AI needs diverse sensors (no single sensor sufficient)
- Perception pipeline: Raw data → Filtering → Fusion → Feature extraction → State estimation
- Diagram shows flow from sensors through to control
- This page covers: LIDAR, Cameras, IMUs, Force/Torque, and Fusion

**Citations**:
- [ROS 2 sensor_msgs](https://docs.ros.org/en/humble/p/sensor_msgs/)

### Section 2: LIDAR - 3D Structure Sensing (550 words)
**Embed**: LIDAR Point Cloud Code + Colab Badge

**Key concepts**:
- Time-of-flight measurement
- Point clouds (sparse 3D structure)
- Range, resolution, FOV trade-offs

**Content outline**:
- **How LIDAR works**:
  - Emit laser pulse, measure time-of-flight
  - Distance = (speed of light × time) / 2
  - Rotate laser to scan 360°
  - Output: Point cloud (N×3 array of [x,y,z] coordinates)

- **Velodyne VLP-16 Example Specifications**:
  | Parameter | Value |
  |-----------|-------|
  | Range | 100m |
  | Accuracy | ±3cm |
  | Channels | 16 |
  | Points/sec | ~300,000 |
  | FOV | 360° horizontal, ±15° vertical |
  | Weight | 830g |
  | Power | 8W |

- **Advantages**:
  - Accurate distance measurements
  - Works in darkness
  - Direct 3D structure

- **Limitations**:
  - Sparse (not dense like images)
  - Expensive ($4,000-$100,000)
  - Moving objects cause motion artifacts

- **Code example**: Simulates LIDAR scan, visualizes 3D point cloud
- **Key insight**: "Robots process ~300,000 points/second for navigation"

**Citations**:
- [Velodyne VLP-16 Datasheet](https://velodynelidar.com/products/puck/) from research.md

### Section 3: Camera Systems - Visual Perception (600 words)
**Embed**: Camera Image Processing Code + Colab Badge

**Key concepts**:
- RGB vs. Depth vs. Stereo cameras
- Resolution, frame rate, latency trade-offs
- Computer vision pipeline

**Content outline**:
- **Camera Types**:
  - **RGB cameras**: Color images, dense visual information
  - **Depth cameras** (Intel RealSense D455): RGB + depth per pixel
  - **Stereo cameras**: Two RGB cameras, compute depth via triangulation

- **Intel RealSense D455 Example Specifications**:
  | Parameter | Value |
  |-----------|-------|
  | Depth Resolution | 1280×720 |
  | RGB Resolution | 1920×1080 |
  | Frame Rate | 30-90 FPS |
  | Depth Range | 0.4m - 6m |
  | Depth Accuracy | <2% at 2m |
  | FOV | 87° × 58° |
  - **Advantages**:
  - Dense visual information (millions of pixels)
  - Color for object recognition
  - Relatively inexpensive ($100-$500)

- **Limitations**:
  - Sensitive to lighting conditions
  - Depth accuracy degrades with distance
  - Reflective/transparent surfaces problematic

- **Processing pipeline**:
  1. Capture RGB image (640×480 typical)
  2. Convert to grayscale (reduce data)
  3. Apply filters (blur, edge detection)
  4. Feature extraction (SIFT, ORB)
  5. Object detection (neural networks)

- **Code example**: Synthetic scene, grayscale conversion, edge detection
- **Real-time requirement**: 30-60 FPS (16-33ms per frame)
- **Key insight**: "Robots process images continuously for navigation and manipulation"

**Citations**:
- [Intel RealSense D455](https://dev.intelrealsense.com/) from research.md

### Section 4: Inertial Measurement Units (IMUs) - Orientation Sensing (550 words)
**Embed**: IMU Orientation Tracking Code + Colab Badge

**Key concepts**:
- Accelerometer + Gyroscope + (Magnetometer)
- Integration for orientation tracking
- Drift accumulation problem

**Content outline**:
- **How IMUs work**:
  - **Accelerometer**: Measures linear acceleration (3 axes)
  - **Gyroscope**: Measures angular velocity (3 axes)
  - **Magnetometer**: Measures magnetic field (compass)

- **Bosch BMI088 Example Specifications**:
  | Parameter | Value |
  |-----------|-------|
  | Gyro Range | ±2000°/s |
  | Gyro Noise | 0.014°/s/√Hz |
  | Accel Range | ±24g |
  | Accel Noise | 175μg/√Hz |
  | Sample Rate | Up to 2kHz |
  | Size | 3×4.5mm |

- **The Drift Problem**:
  - To get orientation: integrate angular velocity over time
  - Orientation(t) = Orientation(t-1) + AngularVelocity × dt
  - Integration accumulates errors → drift
  - Example: After 30 seconds, 20-30° error typical

- **Why drift happens**:
  - Sensor noise (even small noise accumulates)
  - Bias drift (sensor zero-point shifts)
  - Temperature effects

- **Solution**: Sensor fusion with cameras, GPS, or absolute orientation sensors

- **Code example**: Simulates gyroscope, integrates to orientation, shows error accumulation
- **Key insight**: "IMU drift demonstrates why single sensors fail - fusion essential"

**Citations**:
- [Bosch BMI088 Datasheet](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi088/) from research.md

### Section 5: Force/Torque Sensors - Contact Sensing (400 words)
**Key concepts**:
- Measure forces and torques at robot joints/end-effector
- Enable compliant manipulation
- Safety through force limits

**Content outline**:
- **How they work**:
  - Strain gauges measure mechanical deformation
  - 6-axis: 3 forces (Fx, Fy, Fz) + 3 torques (Tx, Ty, Tz)
  - Mounted at wrist or joints

- **ATI Mini45 Example Specifications**:
  | Parameter | Value |
  |-----------|-------|
  | Force Range | ±290N (z-axis) |
  | Torque Range | ±10 Nm |
  | Resolution | 1/20 N (force) |
  | Sampling Rate | Up to 7kHz |
  | Diameter | 45mm |

- **Use cases**:
  - **Grasping**: Detect object contact, control grip force
  - **Assembly**: Detect part insertion, peg-in-hole tasks
  - **Safety**: Detect collisions, limit force to avoid damage

- **Advantages**:
  - Direct measurement of contact
  - Enables compliant control
  - High frequency (kHz)

- **Limitations**:
  - Only measures at sensor location
  - Expensive ($1,000-$10,000)

**Citations**:
- [ATI Force/Torque Sensors](https://www.ati-ia.com/products/ft/ft_models.aspx) from research.md

### Section 6: Multi-Sensor Fusion - Better Together (650 words)
**Embed**: Multi-Sensor Fusion Code + Colab Badge

**Key concepts**:
- Complementary sensor characteristics
- Weighted fusion, Kalman filtering
- Redundancy for reliability

**Content outline**:
- **Why fusion is necessary**:
  - No single sensor is perfect
  - Each sensor has different failure modes
  - Combining sensors: Better accuracy + reliability

- **Example scenario**: Robot measuring distance to obstacle
  - Camera (RealSense): 2% error, 5% miss rate, noise increases with distance
  - LIDAR (Velodyne): ±3cm error, 1% miss rate, consistent across distance
  - Fused estimate: Lower error than either alone

- **Simple fusion: Weighted average**:
  ```
  Fused = w1 × Camera + w2 × LIDAR
  where w1 + w2 = 1
  ```
  - Weights based on sensor reliability
  - Example: w_camera=0.4, w_lidar=0.6 (favor more reliable LIDAR)

- **Advanced fusion: Kalman Filter**:
  - Optimal fusion for Gaussian noise
  - Two steps: Predict (use model) + Update (use measurements)
  - Automatically weights sensors by uncertainty

- **Code example**:
  - Simulates camera and LIDAR measuring distance
  - Shows individual sensor noise and failures
  - Demonstrates weighted fusion improves accuracy by 10-20%
  - Visualization: Individual measurements vs. fused estimate

- **Key insight**: "Sensor fusion is fundamental to Physical AI - single sensors insufficient for robust perception"

**Citations**:
- Sensor specs from previous sections
- [ROS 2 sensor fusion packages](https://docs.ros.org/en/humble/)

## Deep Dive Sections (FR-026)
**Topic 1**: Kalman Filter Mathematics
**Format**: Docusaurus collapsible admonition
**Content**: State prediction equations, measurement update, Kalman gain derivation, why optimal for Gaussian noise

**Topic 2**: Point Cloud Processing Algorithms
**Format**: Docusaurus collapsible admonition
**Content**: RANSAC for plane fitting, ICP for registration, occupancy grids, voxel downsampling

## References Section (FR-012)
- [Velodyne VLP-16 LIDAR](https://velodynelidar.com/products/puck/) - LIDAR specifications
- [Intel RealSense D455](https://dev.intelrealsense.com/) - Depth camera specs
- [Bosch BMI088 IMU](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi088/) - IMU specifications
- [ATI Force/Torque Sensors](https://www.ati-ia.com/products/ft/) - Force sensor specs
- [ROS 2 sensor_msgs](https://docs.ros.org/en/humble/p/sensor_msgs/) - Sensor message types

## Word Count Target
Target: 2,800-3,000 words (longest page, most technical)

## Notes for Implementation
- Each sensor section has specification table (use markdown tables)
- 4 code examples with Colab badges (sensor-noise already in page 2, so 4 new ones here)
- All code examples must be runnable and produce expected output
- Technical accuracy from datasheets (link to official PDFs)
- Emphasize real-time requirements throughout
- Connect to previous pages (why these sensors for Physical AI challenges)
