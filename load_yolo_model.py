import os
from ultralytics import YOLO


def get_latest_video_path(folder):
    videos = [f for f in os.listdir(folder) if f.endswith('.mp4')]
    if not videos:
        raise FileNotFoundError("No video files found in the folder.")

    latest_video = max(
        videos, key=lambda x: os.path.getctime(os.path.join(folder, x)))
    return os.path.join(folder, latest_video)


# Load YOLO model
model = YOLO('licenseplatedetect.pt')

# Define source and run predictions on the latest video in the ./uploads folder
uploads_folder = './uploads'
latest_video_path = get_latest_video_path(uploads_folder)

results = model.predict(latest_video_path, save_crop=True,
                        save=True, imgsz=640, conf=0.75)
