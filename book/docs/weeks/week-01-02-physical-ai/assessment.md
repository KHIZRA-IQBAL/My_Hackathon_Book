---
sidebar_position: 6
title: "Assessment"
description: "Validate your understanding of Physical AI fundamentals"
---

# Week 1-2 Assessment: Physical AI Foundations

## Overview

This assessment validates your understanding of Physical AI fundamentals, embodied intelligence, sensor systems, and the humanoid robotics landscape. It consists of:

- **5 Multiple Choice Questions** (with inline feedback for incorrect answers)
- **3 Short Answer Questions** (with grading rubrics)
- **1 Practical Coding Exercise** (with expected output specification)

Complete all sections and use the provided feedback to self-evaluate. This assessment covers all six learning objectives from the chapter introduction.

---

## Part 1: Multiple Choice Questions (5 questions)

### Question 1: Physical AI Definition

**What is the primary characteristic that distinguishes Physical AI from digital AI systems?**

A) Physical AI uses larger neural networks
B) Physical AI interacts with the real world through sensors and actuators
C) Physical AI requires more training data
D) Physical AI runs on specialized hardware

<details>
<summary><b>Answer</b></summary>

**Correct Answer: B**

**Explanation**: Physical AI is defined by its interaction with the physical world through sensors (perception) and actuators (action). Unlike digital AI that operates purely in software environments, Physical AI must handle noisy sensors, real-time constraints, and physical safety considerations.

**Why other options are incorrect**:
- **A** L Network size is not the defining characteristic. Many digital AI systems (like GPT-4) are extremely large.
- **C** L Data requirements depend on the task, not whether the AI is physical or digital.
- **D** L Both physical and digital AI can use GPUs, TPUs, or specialized hardware.

**Related Content**: See [What is Physical AI?](/docs/weeks/week-01-02-physical-ai/what-is-physical-ai#definition) for the formal definition.

</details>

---

### Question 2: Embodied Intelligence

**According to the concept of embodied intelligence, why does physical form matter for AI systems?**

A) Larger robots can carry more powerful computers
B) Intelligence emerges from body-environment interaction, not just computation
C) Physical forms are easier to manufacture than software systems
D) Humanoid shapes are required for all AI systems

<details>
<summary><b>Answer</b></summary>

**Correct Answer: B**

**Explanation**: Embodied intelligence argues that intelligence is not purely computationalit emerges from the continuous interaction between a physical body, its sensors, its actuators, and the environment. The body actively shapes what problems the agent faces and what solutions are feasible.

**Why other options are incorrect**:
- **A** L Compute power is not the reason form matters. Cloud-connected robots can use remote computing.
- **C** L Manufacturing ease is not related to the concept of embodied intelligence.
- **D** L Embodied intelligence applies to all physical forms, not just humanoids.

**Related Content**: See [Embodied Intelligence](/docs/weeks/week-01-02-physical-ai/embodied-intelligence#introduction-intelligence-beyond-computation) for the full discussion.

</details>

---

### Question 3: Sensor Selection

**A humanoid robot needs to navigate stairs in a dimly lit environment. Which sensor would be MOST appropriate for obstacle detection?**

A) RGB camera (standard color camera)
B) LIDAR
C) Force/torque sensor
D) IMU (accelerometer and gyroscope)

<details>
<summary><b>Answer</b></summary>

**Correct Answer: B**

**Explanation**: LIDAR is an active sensor that emits its own laser light and measures time-of-flight, making it ideal for navigation in darkness. It provides accurate 3D spatial mapping (±3 cm precision for VLP-16) regardless of ambient lighting conditions.

**Why other options are incorrect**:
- **A** L RGB cameras require good lighting to function. They would struggle in dimly lit environments.
- **C** L Force/torque sensors detect contact forces but cannot detect obstacles at a distance. They are used for grasp control, not navigation.
- **D** L IMUs measure orientation and acceleration but cannot detect external obstacles.

**Related Content**: See [LIDAR section](/docs/weeks/week-01-02-physical-ai/sensor-systems#lidar-3d-point-cloud-generation) for LIDAR capabilities.

</details>

---

### Question 4: Sim-to-Real Gap

**Which technique is commonly used to bridge the sim-to-real gap when training robots in simulation?**

A) Using higher resolution graphics in the simulator
B) Domain randomization (varying simulation parameters during training)
C) Training for longer periods in simulation
D) Using more powerful computers for simulation

<details>
<summary><b>Answer</b></summary>

**Correct Answer: B**

**Explanation**: Domain randomization varies simulation parameters (lighting, friction, object sizes, sensor noise) during training to force the policy to be robust to variability. This helps the robot generalize to real-world conditions that differ from simulation.

**Why other options are incorrect**:
- **A** L Graphics quality affects visual realism but does not address physics modeling errors or sensor noise.
- **C** L Training duration does not fix the mismatch between simulated and real physics.
- **D** L Compute power enables faster simulation but does not improve sim-to-real transfer.

**Related Content**: See [Sim-to-Real Gap](/docs/weeks/week-01-02-physical-ai/what-is-physical-ai#bridging-the-gap) for detailed techniques.

</details>

---

### Question 5: Robotics Landscape

**Which humanoid robotics company focuses on end-to-end neural network learning, using a single network to map sensor inputs directly to motor commands?**

A) Boston Dynamics (Atlas)
B) Tesla (Optimus)
C) Agility Robotics (Digit)
D) Sanctuary AI (Phoenix)

<details>
<summary><b>Answer</b></summary>

**Correct Answer: B**

**Explanation**: Tesla Optimus uses end-to-end learning where a single neural network maps camera inputs directly to joint commands. This approach mirrors Tesla's Full Self-Driving (FSD) strategy and aims for generalization across diverse tasks through massive datasets.

**Why other options are incorrect**:
- **A** L Boston Dynamics uses model-based control with optimization-based motion planning, not end-to-end neural networks.
- **C** L Agility Robotics Digit uses a hybrid approach optimized for locomotion, not pure end-to-end learning.
- **D** L Sanctuary AI uses teleoperation to collect demonstration data, then trains policies (hybrid approach).

**Related Content**: See [Tesla Optimus section](/docs/weeks/week-01-02-physical-ai/robotics-landscape#tesla-optimus-end-to-end-neural-network-learning) for details.

</details>

---

## Part 2: Short Answer Questions (3 questions)

### Question 6: Explain the Sim-to-Real Gap

**In 2-3 sentences, explain what the sim-to-real gap is and why it matters for robot learning.**

**Grading Rubric** (5 points total):
- **Definition** (2 points): Clearly states that sim-to-real gap is the difference between simulated physics and real-world dynamics
- **Causes** (2 points): Mentions at least two causes (physics approximations, simplified sensor models, missing variability)
- **Impact** (1 point): Explains why it matters (policies trained in sim may fail in reality)

**Example Strong Answer**:
> The sim-to-real gap refers to the difference between simulated physics and real-world dynamics. Simulations use approximations for friction, contact, and deformation, and often lack realistic sensor noise and environmental variability. This gap matters because a robot trained purely in simulation may fail when deployed in the real world due to unmodeled effects like object slipping, unexpected lighting, or sensor noise.

**Example Weak Answer**:
> The sim-to-real gap is when simulation is different from reality. It matters because the robot might not work.

**What's Missing**: Weak answer lacks specific causes (what makes sim different?) and does not explain transfer challenges.

---

### Question 7: Humanoid Form Factor Justification

**Why is the humanoid form factor important for Physical AI? Provide at least two specific reasons with examples.**

**Grading Rubric** (5 points total):
- **Reason 1 with example** (2 points): e.g., "Human environments designed for human proportions" with example (stairs, door handles)
- **Reason 2 with example** (2 points): e.g., "Tool use" with example (using screwdrivers, brooms)
- **Clarity and specificity** (1 point): Concrete examples, not vague statements

**Example Strong Answer**:
> The humanoid form factor is important because (1) human environments are designed for human proportionsstaircases have 20-30cm steps matching leg length, and door handles are positioned for arm reach, making wheeled or quadruped robots impractical in homes and offices; (2) billions of tools are designed for human hands, so humanoid robots can use existing screwdrivers, brooms, and keyboards without requiring custom tool redesign. This versatility enables operation in unstructured human spaces.

**Example Weak Answer**:
> Humanoids are important because they look like humans and can do tasks.

**What's Missing**: Weak answer provides no specific reasons or examples. "Look like humans" is superficial; "do tasks" applies to any robot.

---

### Question 8: Sensor Fusion Necessity

**Compare LIDAR and camera sensors for robot navigation. Why is multi-sensor fusion necessary instead of using just one sensor type?**

**Grading Rubric** (5 points total):
- **LIDAR strengths/weaknesses** (1.5 points): e.g., accurate 3D, long range, works in dark / no color, expensive
- **Camera strengths/weaknesses** (1.5 points): e.g., high resolution, color, semantic understanding / no direct depth (RGB), limited range (depth cameras)
- **Fusion justification** (2 points): Explains that fusion combines complementary strengths and mitigates individual weaknesses

**Example Strong Answer**:
> LIDAR provides accurate 3D spatial mapping (±3cm for VLP-16) and works in darkness, but lacks color information and is expensive. RGB cameras offer high resolution and semantic understanding (object recognition, texture), but standard cameras provide no depth, and depth cameras have limited range (0.6-6m for RealSense D455). Multi-sensor fusion is necessary because LIDAR provides geometric structure while cameras add semantic meaningtogether they enable both accurate navigation and object recognition, overcoming the limitations of each sensor alone.

**Example Weak Answer**:
> LIDAR is better for some things and cameras are better for other things, so using both is good.

**What's Missing**: Weak answer does not specify what each sensor is better at or why fusion improves performance.

---

## Part 3: Practical Coding Exercise (1 exercise)

### Question 9: Sensor Data Processing and Anomaly Detection

**Task**: You are given simulated sensor data from a robot's LIDAR system. The sensor should measure distances to walls in a rectangular room, but occasionally produces anomalous readings due to sensor glitches.

Write a Python function that:
1. Takes a NumPy array of distance measurements
2. Detects anomalies (readings significantly different from neighbors)
3. Returns the indices of anomalous measurements

**Starter Code**:

```python
import numpy as np

def detect_lidar_anomalies(distances, threshold=2.0):
    """
    Detect anomalous LIDAR measurements.

    Args:
        distances: NumPy array of distance measurements (meters)
        threshold: Standard deviations from local mean to consider anomalous

    Returns:
        anomaly_indices: NumPy array of indices where anomalies occur
    """
    # YOUR CODE HERE
    pass

# Test data: mostly consistent measurements with 2 anomalies
test_distances = np.array([3.0, 3.1, 2.9, 3.0, 15.0, 3.1, 2.9, 3.0, 0.5, 3.0])

anomalies = detect_lidar_anomalies(test_distances, threshold=2.0)
print(f"Anomaly indices: {anomalies}")
print(f"Anomalous values: {test_distances[anomalies]}")
```

**Expected Output**:
```
Anomaly indices: [4 8]
Anomalous values: [15.   0.5]
```

**Implementation Hints**:
- Use a sliding window to compute local mean and standard deviation
- Compare each measurement to its local neighborhood
- Mark measurements that deviate by more than `threshold` standard deviations

**Grading Rubric** (10 points total):
- **Correct algorithm** (4 points): Detects anomalies using statistical methods (local mean, std deviation, or similar)
- **Handles edge cases** (2 points): Works at array boundaries without errors
- **Correct output** (3 points): Identifies the two anomalies in test data
- **Code quality** (1 point): Clear variable names, logical structure

**Example Solution**:

<details>
<summary><b>Show Solution</b></summary>

```python
import numpy as np

def detect_lidar_anomalies(distances, threshold=2.0):
    """
    Detect anomalous LIDAR measurements using local neighborhood comparison.
    """
    anomaly_indices = []
    window_size = 3  # Compare each point to 3 neighbors on each side

    for i in range(len(distances)):
        # Define neighborhood (excluding current point)
        start = max(0, i - window_size)
        end = min(len(distances), i + window_size + 1)
        neighborhood = np.concatenate([distances[start:i], distances[i+1:end]])

        if len(neighborhood) == 0:
            continue

        # Compute local statistics
        local_mean = np.mean(neighborhood)
        local_std = np.std(neighborhood)

        # Check if current measurement is anomalous
        if local_std > 0:
            z_score = abs(distances[i] - local_mean) / local_std
            if z_score > threshold:
                anomaly_indices.append(i)

    return np.array(anomaly_indices)

# Test
test_distances = np.array([3.0, 3.1, 2.9, 3.0, 15.0, 3.1, 2.9, 3.0, 0.5, 3.0])
anomalies = detect_lidar_anomalies(test_distances, threshold=2.0)
print(f"Anomaly indices: {anomalies}")
print(f"Anomalous values: {test_distances[anomalies]}")
```

**Output**:
```
Anomaly indices: [4 8]
Anomalous values: [15.   0.5]
```

**Explanation**: The solution computes a local neighborhood for each measurement (excluding the current point), calculates the mean and standard deviation of that neighborhood, and flags measurements that deviate by more than `threshold` standard deviations. Index 4 (15.0 meters) and index 8 (0.5 meters) are both anomalous compared to the consistent ~3.0 meter readings.

</details>

---

## Self-Evaluation Checklist

After completing the assessment, verify:

- [ ] All 5 MCQs answered (check answers against provided explanations)
- [ ] Short answer 1 includes: definition, causes, and impact of sim-to-real gap
- [ ] Short answer 2 provides 2+ specific reasons with examples for humanoid form factor
- [ ] Short answer 3 compares sensor strengths/weaknesses and justifies fusion
- [ ] Coding exercise correctly identifies anomalies in test data
- [ ] Reviewed incorrect MCQ feedback and revisited related content sections

---

## Answer Key

<!-- Answer Key:
MCQ 1: B (Physical AI interacts with real world)
MCQ 2: B (Intelligence emerges from body-environment interaction)
MCQ 3: B (LIDAR for dark environment navigation)
MCQ 4: B (Domain randomization for sim-to-real)
MCQ 5: B (Tesla Optimus end-to-end learning)
-->

---

## Next Steps

**Congratulations on completing Week 1-2: Physical AI Foundations!**

You now understand:
- The fundamental differences between Physical AI and digital AI
- Why embodied intelligence and physical form matter
- The humanoid robotics landscape and competing technical approaches
- Key sensor systems (LIDAR, cameras, IMUs, force/torque sensors)
- The importance of multi-sensor fusion

**Continue your learning** by exploring advanced topics:
- Week 3-4: Deep learning for robot perception
- Week 5-6: Motion planning and control
- Week 7-8: Reinforcement learning for manipulation

**Stay curious and keep building!**
