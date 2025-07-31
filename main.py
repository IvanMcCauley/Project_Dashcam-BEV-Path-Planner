import cv2
import numpy as np
import math
from config import *
from utils.perspective import get_perspective_transform
from utils.detection import load_model, run_detection
from utils.icons import load_all_icons
from utils.occupancy import build_occupancy_grid
from utils.drawing import draw_path, draw_flag_and_stop, draw_ego_vehicle
from astar import a_star
from utils.lane_lines import draw_lane_lines

# === Load YOLO model and video ===
model = load_model()
cap = cv2.VideoCapture("driving.mp4")

# === Read first valid frame to get dimensions ===
while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("❌ Couldn't read a valid frame.")
        exit()
    frame_h, frame_w = frame.shape[:2]
    break
fps = cap.get(cv2.CAP_PROP_FPS)

# === Setup perspective transform (source trapezoid → top-down grid) ===
M, src = get_perspective_transform(frame_w, frame_h)

# === Load all icons (cars, finish flag, stop sign, ego car) ===
car_icon_right, car_icon_left, cam_car_icon, finish_icon, stop_icon = load_all_icons()

# === Setup video writer for saving output ===
out_w = frame_w + CANVAS_W
out_h = max(frame_h, GRID_H)
out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"XVID"), int(fps), (out_w, out_h))

# === Frame loop starts here ===
cached_results = None
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    annotated = frame.copy()

    # --- Run YOLO detection ---
    yolo_results, cached_results = run_detection(frame, frame_count, model, cached_results)

    # --- Draw YOLO bounding boxes on original frame ---
    for box in yolo_results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        label = f"{model.names[cls_id]} {conf:.2f}"
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # --- Setup BEV canvas ---
    canvas = np.zeros((GRID_H, CANVAS_W, 3), dtype=np.uint8)
    canvas[:, :x_offset] = (30, 30, 30)     # Left margin
    canvas[:, -x_offset:] = (30, 30, 30)    # Right margin

    # --- Draw lane lines ---
    lane_spacing = GRID_W // LANE_COUNT
    draw_lane_lines(canvas, lane_spacing, x_offset)

    # --- Build occupancy grid and draw car icons ---
    occupancy = build_occupancy_grid(cached_results, src, M, x_offset, canvas, car_icon_right, car_icon_left)
    grid_rows = GRID_H // CELL_SIZE

    # --- A* planning from ego position to static goal ---
    start, goal = (grid_rows - 1, 2), (10, 2)
    path = a_star(occupancy, start, goal, allowed_lanes=[2, 3])

    # --- (re)draw lane lines on top (optional double pass) ---
    lane_spacing = GRID_W // LANE_COUNT
    draw_lane_lines(canvas, lane_spacing, x_offset)

    # --- Fallback: if path blocked, just go forward as far as possible ---
    if not path or len(path) < 2:
        for dy in range(1, grid_rows):
            probe = (start[0] - dy, start[1])
            if 0 <= probe[0] < grid_rows and occupancy[probe[0], probe[1]] == 0:
                path = [start, probe]
            else:
                break

    # --- Draw planned path and vehicle visuals ---
    pulse_intensity = int(127 + 128 * math.sin(frame_count * 0.2))
    pulse_color = (0, pulse_intensity, 0)
    draw_path(canvas, path, x_offset, (0, 150, 0), frame_count)
    draw_flag_and_stop(canvas, path, goal, finish_icon, stop_icon, x_offset)
    draw_ego_vehicle(canvas, cam_car_icon, x_offset)

    # --- Merge original + canvas into side-by-side video ---
    canvas_padded = np.zeros((out_h, CANVAS_W, 3), dtype=np.uint8)
    canvas_padded[:GRID_H, :] = canvas
    combined = np.zeros((out_h, out_w, 3), dtype=np.uint8)
    combined[:frame_h, :frame_w] = annotated
    combined[:, frame_w:] = canvas_padded

    # --- Show + save output ---
    cv2.namedWindow("BEV + Path Planning", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("BEV + Path Planning", combined.shape[1], combined.shape[0])
    cv2.imshow("BEV + Path Planning", combined)

    out.write(combined)
    if cv2.waitKey(1) == 27:  # ESC key
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print("✅ Video saved as output.avi")
