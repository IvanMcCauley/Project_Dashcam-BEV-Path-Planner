## Day 1 - Initial setup
- Set up virtual environment & installed ultralytics, OpenCV, torch
- Downloaded city driving video for test data (driving.mp4)
- Created first Python scripts:
  - show_video.py: loads and displays video with OpenCV
  - yolo_detect_print.py: loads YOLOv8, processes each frame, prints detections to console
- Verified pipeline works on ~1800 frames, detects cars and persons with confidence scores
