# Week 1-2 Assessment - Content Outline

## Front Matter
```yaml
---
sidebar_position: 6
title: "Assessment: Test Your Understanding"
description: "Validate your Physical AI knowledge through MCQs, short-answer, and practical coding"
---
```

## Learning Objectives Tested
- All 6 learning objectives from intro page
- Coverage: Physical AI definition, constraints, embodied intelligence, sensor systems, fusion

## Prerequisites (FR-025)
- Completed: All previous 5 pages
- Estimated time: 45 minutes

## Content Structure

### Introduction (150 words)
**Content outline**:
- Congratulations on completing Week 1-2!
- This assessment validates understanding across all topics
- Format: 5 MCQs + 3 short-answer + 1 practical exercise
- MCQs have inline feedback (learn from mistakes)
- Self-grading with answer key at bottom
- Recommended: Complete all 5 pages before starting

---

## Part 1: Multiple Choice Questions (5 questions)

### MCQ 1: Physical AI Definition
**Question**: What is the primary characteristic that distinguishes Physical AI from digital AI?

**Option A**: Physical AI runs on specialized hardware like GPUs
> ❌ Incorrect. All AI can run on GPUs. Physical AI specifically refers to AI systems embodied in robots that interact with the physical world through sensors and actuators. [Review: What is Physical AI](./what-is-physical-ai.md#defining-physical-ai)

**Option B**: Physical AI systems are embodied in robots that perceive and act in the physical environment ✓
> ✅ Correct! Physical AI requires embodiment in a robot with sensors (perception) and actuators (action) to interact with the real world.

**Option C**: Physical AI models are trained on physical datasets rather than synthetic data
> ❌ Incorrect. The term "physical" refers to robotic embodiment and real-world interaction, not the training data source. Digital AI can also train on physical datasets. [Review: Physical vs Digital AI](./what-is-physical-ai.md#physical-vs-digital-ai)

**Option D**: Physical AI is optimized for edge devices and embedded systems
> ❌ Incorrect. While Physical AI may run on edge devices, the defining characteristic is robotic embodiment and physical world interaction, not the deployment platform. [Review: Key Differences](./what-is-physical-ai.md#key-differences)

**Learning Objective Tested**: LO1 - Define Physical AI and distinguish from digital AI

---

### MCQ 2: Embodied Intelligence
**Question**: Why is the humanoid form factor significant for Physical AI applications?

**Option A**: Humanoids are more energy-efficient than wheeled robots
> ❌ Incorrect. Humanoids are actually LESS energy-efficient than wheeled robots. The advantage is versatility in human environments, not efficiency. [Review: Humanoid vs Other Forms](./embodied-intelligence.md#humanoid-vs-other-form-factors)

**Option B**: Humanoids can navigate human-built environments and use existing tools designed for humans ✓
> ✅ Correct! Human environments (stairs, doorways) and tools (hammers, keyboards) are designed for the bipedal human form. Humanoids can use these without modification.

**Option C**: Humanoids have simpler control algorithms than quadrupeds
> ❌ Incorrect. Humanoid control is MORE complex (balance on two legs is harder than four). The advantage is generalization, not simplicity. [Review: Why Humanoid Form](./embodied-intelligence.md#why-the-humanoid-form-factor)

**Option D**: Humanoids are better at outdoor navigation than quadrupeds
> ❌ Incorrect. Quadrupeds like Boston Dynamics Spot excel at outdoor navigation (more stable). Humanoids excel at indoor human environments. [Review: Comparison](./embodied-intelligence.md#humanoid-vs-other-form-factors)

**Learning Objective Tested**: LO4 - Recognize importance of embodied intelligence

---

### MCQ 3: Sensor Systems
**Question**: A robot needs to navigate autonomously in a warehouse that has both good lighting and dark areas. Which sensor combination is most appropriate?

**Option A**: RGB cameras only (rely on good lighting)
> ❌ Incorrect. RGB cameras fail in dark areas. Warehouses have varying lighting, including shadowed regions where cameras struggle. [Review: Camera Limitations](./sensor-systems.md#camera-systems)

**Option B**: LIDAR + depth cameras for complementary strengths ✓
> ✅ Correct! LIDAR works in darkness (active sensing) while cameras provide dense visual info in lit areas. This combination handles all lighting conditions robustly.

**Option C**: IMUs only (orientation sensing sufficient)
> ❌ Incorrect. IMUs only provide orientation (which way robot is facing), not position or obstacle detection. Navigation requires spatial sensing (LIDAR/cameras). [Review: IMU Capabilities](./sensor-systems.md#inertial-measurement-units)

**Option D**: Force/torque sensors for obstacle detection
> ❌ Incorrect. Force sensors detect contact AFTER collision (too late for navigation). Need LIDAR/cameras for preemptive obstacle avoidance. [Review: Force Sensors](./sensor-systems.md#force-torque-sensors)

**Learning Objective Tested**: LO5 - Identify appropriate sensor systems

---

### MCQ 4: Robotics Landscape
**Question**: Which company's approach to humanoid control primarily uses end-to-end neural networks trained on visual data?

**Option A**: Boston Dynamics (Atlas) - uses model predictive control
> ❌ Incorrect. Boston Dynamics uses classical model-based control (MPC + optimization), not end-to-end learning. [Review: Boston Dynamics Approach](./robotics-landscape.md#boston-dynamics)

**Option B**: Tesla (Optimus) - uses vision transformers and end-to-end learning ✓
> ✅ Correct! Tesla's approach leverages vision transformers and end-to-end neural networks, similar to their Full Self-Driving (FSD) system.

**Option C**: Sanctuary AI (Phoenix) - uses teleoperation with human operators
> ❌ Incorrect. While Sanctuary uses teleoperation for data collection, their approach is about learning from human demos, not pure teleoperation. Tesla is the primary end-to-end learning advocate. [Review: Sanctuary Approach](./robotics-landscape.md#sanctuary-ai)

**Option D**: Agility Robotics (Digit) - specialized for bipedal locomotion only
> ❌ Incorrect. Agility uses hybrid control (model-based + learning) focused on locomotion, not pure end-to-end vision-based control. [Review: Agility Approach](./robotics-landscape.md#agility-robotics)

**Learning Objective Tested**: LO2 - Distinguish technical approaches

---

### MCQ 5: Sensor Fusion
**Question**: Why does integrating IMU angular velocity data lead to orientation drift over time?

**Option A**: IMUs have calibration errors that cannot be corrected
> ❌ Incorrect. While calibration matters, the fundamental issue is integration mathematics: noise accumulates when you integrate over time. [Review: Drift Problem](./sensor-systems.md#the-drift-problem)

**Option B**: Integration accumulates sensor noise and bias errors over time ✓
> ✅ Correct! Even small noise in angular velocity (ω) accumulates when integrated: θ(t) = θ(0) + ∫ω dt. Errors compound, causing drift.

**Option C**: IMU sampling rates are too low for accurate tracking
> ❌ Incorrect. IMUs sample at kHz rates (very high frequency). The problem is mathematical (integration accumulates error), not sampling rate. [Review: IMU Specs](./sensor-systems.md#bosch-bmi088)

**Option D**: Magnetic interference corrupts the gyroscope measurements
> ❌ Incorrect. Magnetic fields affect magnetometers, not gyroscopes. Gyroscopes measure angular velocity mechanically (MEMS). The drift issue is integration-based. [Review: How IMUs Work](./sensor-systems.md#how-imus-work)

**Learning Objective Tested**: LO3 - Understand integration error accumulation

---

## Part 2: Short Answer Questions (3 questions)

### Short Answer 1: Sim-to-Real Gap
**Question**: In 2-3 sentences, explain the sim-to-real gap and why it presents a challenge for Physical AI development.

**Grading Rubric** (10 points):
- **Definition** (4 pts): Sim-to-real gap is the difference between simulated robot behavior and real-world performance
- **Why it exists** (3 pts): Physics engines approximate reality; real world has complexities simulation doesn't capture (friction, compliance, sensor noise)
- **Impact** (3 pts): Policies trained in simulation may fail in reality, requiring domain randomization or real-world fine-tuning

**Example strong answer**:
"The sim-to-real gap is the mismatch between a robot's performance in simulation versus reality. It exists because physics simulators approximate real-world dynamics—they don't perfectly model friction, contact forces, and sensor noise. This means control policies trained in simulation (e.g., NVIDIA Isaac Sim) often fail when deployed to physical robots, requiring techniques like domain randomization to improve transfer."

**Key concepts to include**:
- Simulation vs. reality mismatch
- Physics approximations
- Training-deployment failure mode
- Mitigation strategies (domain randomization, noise injection)

**Learning Objective Tested**: LO3 - Understand sim-to-real challenges

---

### Short Answer 2: Sensorimotor Loops
**Question**: Explain why sensorimotor loops (perception-action cycles) are essential for humanoid robots operating in unstructured environments. Provide a specific example.

**Grading Rubric** (10 points):
- **Definition** (3 pts): Sensorimotor loop = Sense → Process → Act → Environment changes → Sense (repeat)
- **Why essential** (4 pts): Cannot pre-plan all actions (environment uncertain); must adapt in real-time based on feedback
- **Example** (3 pts): Concrete scenario showing closed-loop control (e.g., walking on uneven terrain, grasping deformable objects)

**Example strong answer**:
"Sensorimotor loops enable real-time adaptation to unpredictable environments. Unlike factory robots with pre-programmed sequences (open-loop), humanoids need continuous sensory feedback to adjust actions. For example, when Atlas walks on rubble, its foot placement must adjust mid-step based on ground contact sensors and IMU feedback. Without this closed-loop control, the robot would fall when terrain differs from expectations."

**Key concepts to include**:
- Real-time feedback
- Open-loop vs. closed-loop
- Adaptation to uncertainty
- Specific example showing perception→action→adaptation

**Learning Objective Tested**: LO4 - Understand embodied intelligence principles

---

### Short Answer 3: Sensor Selection
**Question**: Compare LIDAR and depth cameras for robot navigation. When would you choose one over the other?

**Grading Rubric** (10 points):
- **LIDAR advantages** (3 pts): Long range, works in darkness, consistent accuracy
- **Camera advantages** (2 pts): Dense visual info, less expensive, color for recognition
- **LIDAR limitations** (2 pts): Expensive, sparse point cloud
- **Camera limitations** (2 pts): Lighting-dependent, depth accuracy degrades with distance
- **Selection criteria** (1 pt): Use case determines choice

**Example strong answer**:
"LIDAR provides accurate 3D structure up to 100m and works in total darkness, but is expensive ($4k+) and produces sparse point clouds. Depth cameras (Intel RealSense) give dense visual information at lower cost ($200), but only work to ~6m and struggle in darkness or bright sunlight. Choose LIDAR for outdoor long-range navigation (autonomous vehicles); choose depth cameras for indoor manipulation tasks with good lighting (home robots). Best solution: Use both for complementary strengths."

**Key concepts to include**:
- Range, cost, lighting requirements
- Dense vs. sparse data
- Use case examples
- Recognition that fusion often best

**Learning Objective Tested**: LO5 - Evaluate sensor trade-offs

---

## Part 3: Practical Coding Exercise (1 exercise)

### Practical Exercise: Sensor Data Filtering
**Instructions**:
You have a noisy distance sensor (simulated below) measuring obstacle distance. The sensor has Gaussian noise with std=0.2m and occasional outliers (> 3σ).

1. Load the provided sensor data
2. Implement a simple moving average filter (window=5)
3. Implement outlier rejection (reject readings > 3σ from mean)
4. Plot: raw data, filtered data, and ground truth
5. Calculate and report RMSE before/after filtering

**Starter code**:
```python
import numpy as np
import matplotlib.pyplot as plt

# Simulated sensor data (100 measurements)
np.random.seed(42)
true_distance = 3.5  # meters
measurements = np.random.normal(true_distance, 0.2, 100)

# Add 5 outliers
outlier_indices = np.random.choice(100, 5, replace=False)
measurements[outlier_indices] += np.random.uniform(1.0, 2.0, 5)

# TODO: Implement your solution here
```

**Expected output specification**:
- Plot showing 3 lines: raw (noisy), filtered (smooth), ground truth (horizontal line)
- Print statement: "RMSE before filtering: X.XXX m"
- Print statement: "RMSE after filtering: Y.YYY m"
- RMSE should improve by ~30-50%

**Grading Rubric** (20 points):
- **Moving average filter** (7 pts): Correct implementation using np.convolve or manual loop
- **Outlier rejection** (7 pts): Identifies and removes/replaces measurements > 3σ
- **Visualization** (3 pts): Clear plot with labeled axes, legend, title
- **RMSE calculation** (3 pts): Correct formula: sqrt(mean((predicted - true)^2))

**Solution approach**:
```python
# Moving average filter
def moving_average(data, window=5):
    return np.convolve(data, np.ones(window)/window, mode='valid')

# Outlier rejection
def reject_outliers(data, threshold=3):
    mean = np.mean(data)
    std = np.std(data)
    filtered = data.copy()
    outliers = np.abs(data - mean) > threshold * std
    filtered[outliers] = mean  # Replace outliers with mean
    return filtered

# Apply filters
data_no_outliers = reject_outliers(measurements)
filtered_data = moving_average(data_no_outliers)

# Calculate RMSE
rmse_before = np.sqrt(np.mean((measurements - true_distance)**2))
rmse_after = np.sqrt(np.mean((filtered_data - true_distance)**2))

print(f"RMSE before: {rmse_before:.3f} m")
print(f"RMSE after: {rmse_after:.3f} m")
```

**Learning Objective Tested**: LO6 - Implement sensor processing

---

## Answer Key Section (FR-023)

```html
<!-- ANSWER KEY - Week 1-2 Assessment

Part 1: Multiple Choice
Q1: B - Physical AI embodied in robots interacting with physical world
Q2: B - Humanoids navigate human environments and use existing tools
Q3: B - LIDAR + depth cameras for complementary strengths
Q4: B - Tesla uses vision transformers and end-to-end learning
Q5: B - Integration accumulates sensor noise over time

Part 2: Short Answer Grading Rubrics
See individual rubrics above for scoring guidelines.
Key concepts to check:
- SA1: Simulation-reality mismatch, physics approximations, domain randomization
- SA2: Real-time feedback, closed-loop control, specific example
- SA3: LIDAR vs camera trade-offs, use case selection

Part 3: Practical Exercise
Check for:
- Moving average implementation
- Outlier rejection (> 3σ)
- Correct RMSE calculation
- Clear visualization
Expected RMSE improvement: 30-50%

Total Points: 50 + 30 + 20 = 100 points

Passing score: 70/100

-->
```

## References Section (FR-012)
- All previous pages serve as references
- Students should review specific pages based on incorrect answers
- Links embedded in inline feedback

## Word Count Target
Target: 1,800-2,000 words (including question text, feedback, rubrics)

## Notes for Implementation
- MCQ feedback must link back to specific content sections
- Short-answer rubrics must be specific and measurable
- Practical exercise must be runnable with starter code provided
- Answer key in HTML comment at bottom (hidden from students)
- Encourage self-assessment ("Did I meet the rubric criteria?")
- Provide "Further Study" section with links to advanced topics
