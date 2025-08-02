# 🧠 Dashcam BEV Path Planner

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white" alt="OpenCV">
  <img src="https://img.shields.io/badge/YOLOv8-ultralytics-orange" alt="YOLOv8">
  <img src="https://img.shields.io/badge/A*%20Pathfinding-blueviolet" alt="A* Pathfinding">
  <img src="https://img.shields.io/badge/BEV-Mapping-brightgreen" alt="BEV Mapping">
  <img src="https://img.shields.io/badge/Torch-EE4C2C?logo=pytorch&logoColor=white" alt="Torch">
  <img src="https://img.shields.io/badge/Numpy-013243?logo=numpy&logoColor=white" alt="Numpy">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
</p>



<table>
  <tr>
    <td style="vertical-align: top; padding-right: 20px;">
      <p>
        A real-time simulation of <strong>autonomous driving logic</strong>, from dashcam video to vehicle detection, Bird’s Eye View projection, occupancy grid mapping, and A* path planning.
      </p>
      <p>
        This project emulates the core decision-making pipeline found in self-driving systems:<br>
        <strong>Perception → Mapping → Planning.</strong>
      </p>
    </td>
    <td style="vertical-align: top;">
      <img src="output_gif2.gif" width="270" alt="BEV Path Planning Output">
    </td>
  </tr>
</table>

---

## 🚗 Project Goal

To simulate the key control loop of an autonomous vehicle:

- Detect surrounding vehicles from dashcam footage using a neural network
- Convert detections into a **Bird’s Eye View (BEV)** representation of the road
- Run **A\*** path planning to determine a safe route forward based on obstacles

This demonstrates core skills in **computer vision, spatial transformation**, and **motion planning**, all fundamental to real-world autonomous driving systems.

---


## 🌍 Context

Autonomous vehicles don’t just detect objects, they **reason about space and motion**.  
This project emulates that reasoning:

- What’s around me? → YOLOv8 object detection
- What’s drivable? → BEV projection into occupancy grid
- Where can I go? → A* path planning in real time

It’s a simulation of the perception → planning loop used in real-world AV stacks like Apollo, Autoware, and CARIAD.

---

## 🧩 Features

### ✅ Object Detection (Perception)
- Uses **YOLOv8** to detect vehicles in real time
- Bounding boxes rendered with class labels and confidence
- Results cached to ensure consistent multi-frame tracking

### ✅ BEV Projection & Occupancy Grid
- Manually tuned **trapezoidal ROI** projects perspective into a top-down grid
- Lane dividers (white and yellow) simulate a 4-lane road
- Grid shows non-drivable margins for realistic layout


### ✅ A* Path Planning
- A* search runs on the binary occupancy grid
- Chooses safest path in real time using only lanes 2 & 3 (center-right)
- If no clear path is found, a **stop sign** appears to indicate blockages

### ✅ Icon-Based Visualization
- Vehicles overlaid as **directional icons** (flipped by lane side)
- Ego vehicle drawn at bottom of BEV
- Icons pasted using **alpha blending** to preserve visuals

### ✅ Pulsing Path Animation
- Path drawn as a flowing sequence of bright pulses, simulating “intent”
- Brightness cycles frame-by-frame using a sine wave function
- Adds intuitive visualization of forward motion logic (like AV stack visualizers)

### ✅ Modular Design
- Fully modular: each subsystem (perception, projection, planning, rendering) is in its own file
- Mirrors industry architecture found in systems like Apollo, Autoware, and CARIAD
- Easy to replace A* with other planners (e.g. Hybrid A*, RRT*)

---

## 🧠 How This Reflects Real AV Systems

This project simulates the **actual logic** used by modern autonomous vehicles:

- **BEV Mapping** is used by Tesla, Mobileye, Waymo, and nearly every AV stack
- **Occupancy Grids** are a cornerstone of sensor fusion and decision-making
- **A\*** is still used in hybrid planners, fallback routes, and behavioral logic
- The process of converting 2D detections → world coordinates is essential for **planning and control**

Though simplified, the system follows the same principles used in full-scale autonomous driving software.

---
### 📄 File Overview

| File | Description |
|------|-------------|
| [main.py](main.py) | Core execution file — runs detection, BEV, and path planning |
| [config.py](config.py) | Central config file for all constants and parameters |
| [astar.py](astar.py) | A* pathfinding algorithm for lane-aware planning |
| [detection.py](detection.py) | Runs YOLOv8 inference and handles result caching |
| [perspective.py](perspective.py) | Applies trapezoid-to-BEV perspective transform |
| [occupancy.py](occupancy.py) | Builds binary occupancy grid and places car icons |
| [drawing.py](drawing.py) | Renders path, ego vehicle, stop sign, and flag |
| [icons.py](icons.py) | Loads and resizes all UI icons (cars, signs) |
| [lane_lines.py](lane_lines.py) | Draws lane dividers with optional highlighting |
| [driving.mp4](https://drive.google.com/file/d/1cbK9gPL7cW_nIEsJKrfM6FUGHA9mbdPG/view?usp=sharing) | Dashcam input video used for detection |
| [requirements.txt](requirements.txt) | Python dependencies for easy setup |
| [LOG.md](LOG.md) | Full development log with step-by-step progress |
| [README.md](README.md) | Project overview and setup instructions |

---

## 📂 File Structure
```
yolo_adas_project/
│
├── 🧠 main.py     ← Core execution file
├── ⚙️ config.py     ← All constants and parameters
├── 🔍 astar.py     ← A* pathfinding algorithm
│
├── 🧩 utils/
│ ├── detection.py     ← YOLOv8 detection and caching
│ ├── perspective.py     ← Trapezoid warp logic for BEV
│ ├── occupancy.py     ← Occupancy grid generation
│ ├── drawing.py     ← Path drawing, icons, stop sign
│ ├── icons.py     ← Icon loading and blending
│ ├── lane_lines.py     ← Lane line rendering
│
├── driving.mp4     ← Dashcam input 
├── output.avi     ← Final video output (saves to directory when program finishes running)
├── requirements.txt     ← Python dependencies for easy setup
├── LOG.md     ← Full dev log (linked below)
└── README.md     ← This file
```


---


---

## 📓 Development Log

Every step of the build — from detection and BEV projection to A* debugging and icon rendering — was tracked day-by-day in the [**LOG.md**](./LOG.md).

Useful if you're curious about the process, want to recreate it, or build on top of it.

---



## ▶️ Demo Video

📹 **[Click here to watch the live demo →](https://drive.google.com/file/d/1lvMLDSJ1ULKqPAdVSpwMIgijDAfISJai/view?usp=sharing)**  
Watch the full pipeline in motion — from raw dashcam input to BEV pathfinding overlay.

---

## ⚠️ Notes on Running

This system is tuned for the provided `driving.mp4`. The perspective transform is manually calibrated for this video.

If you use your own footage:
- Update the trapezoid corners in `utils/perspective.py`
- Ensure your video resolution matches or update `config.py`

---

## 💻 Setup Instructions

1. Clone this repo
```
git clone https://github.com/IvanMcCauley/Project_Dashcam-BEV-Pat-hPlanner.git
```

3. (Optional) Replace driving.mp4 with your own dashcam video
   - Note: trapezoid settings must be manually tuned

4. Install dependencies
```
pip install -r requirements.txt
```

4. Run the simulation
```
python main.py
```

---
## 💡 What I Learned

- Translating computer vision into real-time planning logic
- Implementing A* from scratch and debugging edge cases
- Designing a modular codebase that mirrors real AV architecture
- Visual communication of intent, making AV decision-making interpretable
- Managing detection noise and ensuring stability frame-to-frame

---

## 🚧 Why I Built This Project

Built independently after graduating in Mechatronic Engineering,  
this project is part of my ongoing journey into **Autonomous Vehicles** and **ADAS systems**.

I'm deeply interested in how real autonomous stacks work - perception, mapping, and motion planning, so I’m creating hands-on simulations that reflect those exact principles.

Each build is both a learning experience and a step toward contributing to real-world autonomy.


---

## 👤 Built By

**Ivan McCauley**  
[🔗 Connect on LinkedIn](https://www.linkedin.com/in/ivan-mccauley)


