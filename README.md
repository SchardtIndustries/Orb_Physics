# 🌀 Dots Physics Simulation App

## Overview
The **Dots App** is an interactive 2D physics simulation built with **cmu_graphics**.  
It models collisions, motion, and simple gravitational interactions between moving circular particles (“dots”) inside a bounded region. The program visually demonstrates principles of Newtonian mechanics such as inertia, elastic collision response, and gravitational attraction — all with dynamic visuals and particle effects.

---

## Core Features

### 🎯 Interactive Dot Creation
- Click anywhere inside the board to spawn a new dot.  
- Use different **modes** to create dots with distinct physical properties:
  - **Standard Blue Dot** — medium size and speed, baseline physics.
  - **Big Slow Red Dot** — heavy, slow-moving, and durable.
  - **Fast Sienna Dot** — lightweight and fast, with wrap-around edges.

### 💥 Collision System
- Elastic, momentum-conserving collisions.
- Sparks and cracks appear upon impact.
- Dots take gradual damage until they break apart.
- “I-frames” prevent instant multiple hits.

### 🌌 Gravity Modes
Toggle with the **G** key:
1. **None** – free motion, no gravity  
2. **Mutual** – all dots attract each other  
3. **Fall** – downward planetary gravity

### 🧱 Wall Behavior
- Blue/red dots bounce off walls.
- Sienna dots wrap around screen edges.

---

## Physics Details
- Multi-substep integration for stable simulation.  
- Elastic impulse response and position correction.  
- Anti-sticking bias to prevent overlapping dots.  
- Speed clamping for numerical stability.

---

## Visual Effects
- Cracks form on impact and accumulate as damage.
- Sparks fade dynamically for a realistic metallic look.

---

## UI & Controls

| Action | Key / Mouse | Description |
|--------|--------------|-------------|
| 🖱 Click | Inside board | Spawn a new dot |
| **M** | Change dot mode | Cycle between dot types |
| **C** | Clear all | Remove all dots and sparks |
| **G** | Toggle gravity | Switch between modes |
| **Resize window** | — | Board scales dynamically |

---

## Technical Highlights
- Object-oriented design using Python classes.
- Real-time physics at ~60 FPS.
- Dynamic resizing with `onResize()`.
- Inheritance and polymorphism in dot types.

---

## Educational Value
A demonstration of **object-oriented programming** and **2D physics simulation**.  
Combines geometry, motion, and elastic collision response in an engaging interactive environment — great for students learning computer science, game physics, or simulation fundamentals.

---

## Running the App
You’ll need:
- `cmu_graphics` (install via `pip install cmu-graphics`)
- Python 3.9+

Then run:
```bash
python DotsApp.py
