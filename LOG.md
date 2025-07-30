## Day 1 - Initial setup
- ✅ Set up virtual environment & installed ultralytics, OpenCV, torch
- ✅ Downloaded city driving video for test data (driving.mp4)
- ✅Created first Python scripts:
  - show_video.py: loads and displays video with OpenCV
  - yolo_detect_print.py: loads YOLOv8, processes each frame, prints detections to console
- ✅ Verified pipeline works on ~1800 frames, detects cars and persons with confidence scores

## Day 2–4 - BEV Pipeline, Trapezoid Warp, and Occupancy Grid

- ✅ Designed and finalized trapezoid ROI for BEV transformation using real dashcam perspective (manually tuned until alignment was “perfect”)
- ✅ Implemented perspective transform with `cv2.getPerspectiveTransform()` and `cv2.warpPerspective()` to create top-down Bird’s Eye View (BEV)
- ✅ Scaled trapezoid coordinates relative to actual video resolution
- ✅ Created binary BEV occupancy grid of shape 150×1500 pixels (height matches road depth, width spans 4 lanes)
- ✅ Defined 4-lane layout and color-coded lane dividers in BEV:
  - Center line = yellow, others = white
  - Footpath margins shaded gray to indicate non-drivable areas

## Day 5 - Vehicle Projection and Icon Overlay

- ✅ Projected YOLO-detected vehicle centroids (bottom center of box) from original frame to BEV using `cv2.perspectiveTransform()`
- ✅ Implemented directional car icon overlay:
  - Vehicles in right-side lanes show standard icon
  - Vehicles in left-side lanes use flipped icon
- ✅ Added perspective-aware Y-stretching for visual realism in BEV
- ✅ Used `pointPolygonTest()` to filter out detections outside trapezoid ROI

## Day 6 - Display Optimization and Real-Time Output

- ✅ Refactored display logic to use `matplotlib` for live side-by-side visualization:
  - Left: Original frame with trapezoid and YOLO boxes + labels
  - Right: BEV occupancy grid with vehicle overlays
- ✅ Synced occupancy grid updates to every 4 frames, later adjusted to every 2 frames for smoother responsiveness
- ✅ Preserved full-frame-rate video output using OpenCV’s `VideoWriter`, ensuring annotations remain visible on every frame

## Day 7 - Finishing Touches

- ✅ Restored full YOLO bounding box and confidence label rendering on each frame
- ✅ Ensured icons paste correctly using alpha blending
- ✅ Final script (`side_by_side_bev.py`) now saves `output.avi` with side-by-side view: original + BEV
- ✅ Code modularized with clean functions for `stretch_y()`, `load_icon()`, `paste_icon()`
 
## Day 8–11 – A* Path Planning Integration
- ✅ Implemented A* algorithm from scratch in astar.py using Manhattan distance and grid-based neighbors-
- ✅ Defined start point as ego vehicle in bottom-center of lane 2; goal as fixed location at end of lane 2
- ✅ Allowed path planning only within "safe" lanes (lane 2 & 3) to simulate lane discipline
- ✅ Converted A* path from grid coordinates to pixel coordinates and overlaid path on BEV canvas
- ✅ Implemented fallback logic: if no valid path to goal, draw a short path forward

## Day 12 – Flag and Stop Sign Visual Feedback

- ✅ Always rendered checkered flag icon at fixed goal position in BEV grid
- ✅ Added dynamic stop sign overlay if A* path could not reach goal:
  - Positioned at final reachable node
  - Only visible when goal is blocked
- ✅ Implemented alpha blending for both flag and stop sign icons to support transparency

## Day 13 – Ego Car and Layout Finalization

- ✅ Added ego vehicle icon at bottom of BEV grid using CAM_CAR.PNG
- ✅ Positioned in lane 2 using pixel-based placement aligned with occupancy grid
- ✅ Fixed draw order so ego vehicle, lane lines, and stop signs don't obscure each other
- ✅ Tweaked margins, spacing, and grid offset for clean visual composition

## Day 14 – Aesthetic Polish & Animation
- ✅ Added pulsing animation to A* path using sine wave brightness modulation:
  - Achieved dynamic “speed boost pad” visual using time-dependent oscillation
  - Customizable pulse speed and direction via frame_count
- ✅ Preserved original path behavior and grid alignment
- ✅ Fine-tuned pulse smoothness for visual clarity without distraction

## Day 15 – Final Testing & Cleanup
- ✅ Verified full system from raw video to final annotated output works end-to-end
- ✅ Removed deprecated scripts (yolo_detect_print.py, show_video.py, early test files)
- ✅ Confirmed main.py + utils/ + config.py are only required scripts
- ✅ Final output saved as output.avi with:
  - Live YOLO detections
  - Accurate BEV projection
  - Obstacle-aware A* path planning
  - Dynamic stop logic
  - Clean, stylized visuals ready for portfolio
