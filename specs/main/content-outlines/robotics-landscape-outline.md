# Humanoid Robotics Landscape - Content Outline

## Front Matter
```yaml
---
sidebar_position: 4
title: "The Humanoid Robotics Landscape"
description: "Survey of leading humanoid robotics companies and their technical approaches"
---
```

## Learning Objectives (FR-024)
1. Identify 5 major humanoid robotics companies and their flagship robots
2. Distinguish between teleoperation, learning-based, and model-based control approaches
3. Understand the trade-offs between different technical approaches
4. Recognize industry trends and commercial applications
5. Evaluate which approach is best suited for different use cases

## Prerequisites (FR-025)
- Completed: Introduction, What is Physical AI, Embodied Intelligence
- Estimated time: 40 minutes

## Content Structure

### Section 1: Industry Overview (300 words)
**Embed**: Robotics Landscape Mermaid diagram

**Key concepts**:
- 2023-2025 breakthrough period
- Three main approaches: Teleoperation→AI, End-to-End Learning, Model-Based Control, Hybrid
- Funding surge and commercial deployments beginning

**Content outline**:
- Why now? Foundation models, better hardware, increased funding
- Market segments: Manufacturing, warehousing, home assistance
- Diagram categorizes 5 companies by approach

**Citations**:
- Company official announcements from research.md

### Section 2: Boston Dynamics - Atlas (Model-Based Control) (450 words)
**Embed**: YouTube video - Atlas parkour demo

**Key concepts**:
- Hydraulic → Electric transition (April 2024)
- Model Predictive Control (MPC)
- Perception-driven behaviors

**Content outline**:
- **Company background**: Founded 1992, acquired by Hyundai 2021
- **Atlas specifications**:
  - Height: ~1.5m, Weight: 89kg (hydraulic version)
  - Electric version: Expanded range of motion

- **Technical approach: Model-Based Control**
  - Classical control theory + optimization
  - Model Predictive Control (MPC): Predict future states, optimize actions
  - Real-time perception updates behavior
  - NOT pre-programmed routines (adapts to environment)

- **Capabilities demonstrated**:
  - Parkour: Jumps, vaults, backflips
  - Tool use: Carrying construction materials, operating power tools
  - Complex balancing using all four limbs

- **Pros**: Reliable, explainable, works immediately
- **Cons**: Requires expert tuning, difficult to generalize to new tasks

**Video**: Can't see the video? [Watch Atlas Parkour on YouTube](URL_from_research.md)

**Citations**:
- [Boston Dynamics Official](https://bostondynamics.com/products/atlas/)
- April 2024 electric Atlas announcement from research.md

### Section 3: Tesla - Optimus (End-to-End Learning) (450 words)
**Embed**: YouTube video - Optimus latest demo

**Key concepts**:
- Vision transformers
- End-to-end neural networks (pixels → actions)
- Leveraging FSD experience

**Content outline**:
- **Company background**: Announced August 2021 (AI Day)
- **Optimus specifications**:
  - Height: ~1.73m (5'8"), Weight: ~73kg
  - 28 degrees of freedom
  - FSD computer (custom AI chip)

- **Technical approach: End-to-End Learning**
  - Neural networks learn perception→action mapping
  - Vision transformers process camera inputs
  - Learns from demonstration and simulation
  - Leverages Tesla's FSD (Full Self-Driving) AI experience

- **Capabilities demonstrated** (as of latest demo):
  - Walking on various terrains
  - Object manipulation (sorting, folding)
  - Autonomous navigation

- **Pros**: Scales with data, generalizes better than hand-tuned control
- **Cons**: "Black box", requires massive training data, unpredictable failures

**Video**: Can't see the video? [Watch Tesla Optimus Demo on YouTube](URL_from_research.md)

**Citations**:
- [Tesla AI Page](https://www.tesla.com/AI)
- AI Day presentations from research.md

### Section 4: Figure AI - Figure 01 (Hybrid: Foundation Models + Control) (450 words)
**Embed**: YouTube video - OpenAI integration demo

**Key concepts**:
- Foundation models for reasoning
- Integration with OpenAI
- Commercial focus (BMW partnership)

**Content outline**:
- **Company background**: Founded 2022, raised $675M (March 2024)
- **Figure 01 specifications**:
  - Height: ~1.7m, Weight: ~60kg
  - Deployment: BMW manufacturing (commercial pilot)

- **Technical approach: Hybrid (Foundation Models + Control)**
  - Large language models (LLMs) for high-level reasoning
  - Vision-language models for scene understanding
  - Traditional control for low-level execution
  - OpenAI partnership: GPT-4 integration

- **Capabilities demonstrated**:
  - Natural language interaction ("Can you give me something to eat?")
  - Multi-step task execution
  - Object recognition and manipulation

- **Pros**: Human-like reasoning, adaptable to novel instructions
- **Cons**: LLM latency, requires robust low-level control layer

**Video**: Can't see the video? [Watch Figure + OpenAI Demo on YouTube](URL_from_research.md)

**Citations**:
- [Figure AI Official](https://figure.ai/)
- BMW partnership announcement from research.md

### Section 5: Sanctuary AI - Phoenix (Teleoperation to Autonomy) (400 words)
**Embed**: YouTube video - Phoenix demo

**Key concepts**:
- Carbon™ AI control system
- Teleoperation for data collection
- Gradual autonomy increase

**Content outline**:
- **Company background**: Founded 2018, Canadian
- **Phoenix (7th generation) specifications**:
  - Height: ~1.7m
  - Focus: Human-like dexterity

- **Technical approach: Teleoperation → AI**
  - Humans teleoperate robot to demonstrate tasks
  - AI learns from human demonstrations
  - Gradually increase autonomy as policy improves
  - Carbon™ AI: Proprietary control system

- **Capabilities demonstrated**:
  - Retail environment tasks (stocking shelves)
  - Fine manipulation (picking small objects)

- **Pros**: Rapid task learning, human expertise encoded
- **Cons**: Requires human operators initially, scalability questions

**Video**: Can't see the video? [Watch Sanctuary Phoenix Demo on YouTube](URL_from_research.md)

**Citations**:
- [Sanctuary AI Official](https://sanctuary.ai/)

### Section 6: Agility Robotics - Digit (Locomotion-Focused Hybrid) (400 words)
**Embed**: YouTube video - Digit warehouse demo

**Key concepts**:
- Bipedal locomotion specialist
- Commercial deployments (Amazon, GXO)
- Purpose-built for logistics

**Content outline**:
- **Company background**: Spun out of Oregon State University 2015
- **Digit specifications**:
  - Height: ~1.75m
  - Payload: 16kg
  - Battery: 2-4 hours runtime

- **Technical approach: Locomotion Specialist**
  - Hybrid model-based + learning for walking
  - Simplified upper body (no fine manipulation focus)
  - Optimized for: Walking, carrying, placing

- **Capabilities demonstrated**:
  - Warehouse tote handling
  - Stair climbing
  - Uneven terrain navigation

- **Pros**: Commercial deployments already, proven reliability
- **Cons**: Limited manipulation vs. full humanoids

**Video**: Can't see the video? [Watch Digit Warehouse Demo on YouTube](URL_from_research.md)

**Citations**:
- [Agility Robotics Official](https://agilityrobotics.com/)
- Amazon partnership from research.md

### Section 7: Comparison and Future Outlook (350 words)
**Key concepts**:
- No clear "winner" yet
- Convergence likely (all approaches borrowing from each other)
- Next 5 years critical for commercialization

**Content outline**:
- **Comparison table**:
  | Company | Approach | Strength | Use Case |
  |---------|----------|----------|----------|
  | Boston Dynamics | Model-Based | Reliability | Research, Inspection |
  | Tesla | End-to-End Learning | Scalability | Manufacturing, Home |
  | Figure AI | Foundation Models | Reasoning | Manufacturing |
  | Sanctuary | Teleoperation→AI | Rapid Learning | Retail, Service |
  | Agility | Locomotion Focus | Commercial Ready | Logistics |

- **Trend**: Hybrid approaches winning
- **Challenges ahead**: Safety certification, cost reduction, battery life
- **Timeline**: Expect commercial deployments 2025-2030

## Deep Dive Sections (FR-026)
**Topic**: Comparing Control Approaches - Trade-offs
**Format**: Docusaurus collapsible admonition
**Content**: Detailed technical comparison of MPC vs. end-to-end learning vs. hybrid approaches, mathematical foundations, when to use each

## References Section (FR-012)
- [Boston Dynamics Atlas](https://bostondynamics.com/products/atlas/) - Model-based control leader
- [Tesla AI](https://www.tesla.com/AI) - End-to-end learning approach
- [Figure AI](https://figure.ai/) - Foundation model integration
- [Sanctuary AI](https://sanctuary.ai/) - Teleoperation to autonomy
- [Agility Robotics](https://agilityrobotics.com/) - Commercial bipedal platform

## Word Count Target
Target: 2,300-2,500 words

## Notes for Implementation
- All 5 YouTube videos must have iframe embeds + fallback links
- Diagram shows categorization by approach
- Maintain neutral tone (no company endorsements)
- Technical accuracy from official company sources
- Update specifications from latest official announcements
