### IMAGE VERSION ###
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ultralytics import YOLO
import cv2
import numpy as np

from sort.sort import *
from util import get_car, read_license_plate, write_csv

# Load YOLO models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('./models/license_plate_detector.pt')

# Load image
image_path = './sample/sample_image.jpg'
frame = cv2.imread(image_path)

# Prepare results dictionary
results = {}
frame_nmr = 0
results[frame_nmr] = {}

# === Detect Vehicles
vehicles = [2, 3, 5, 7]  # car, motorcycle, bus, truck
detections = coco_model(frame)[0]
detections_ = []
for detection in detections.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = detection
    if int(class_id) in vehicles:
        detections_.append([x1, y1, x2, y2, score])
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

# === Detect License Plates
track_ids = Sort().update(np.array(detections_))
license_plates = license_plate_detector(frame)[0]

for license_plate in license_plates.boxes.data.tolist():
    x1, y1, x2, y2, score, class_id = license_plate
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

    xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

    if car_id != -1:
        license_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
        license_crop_gray = cv2.cvtColor(license_crop, cv2.COLOR_BGR2GRAY)
        _, license_crop_thresh = cv2.threshold(license_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

        license_text, license_text_score = read_license_plate(license_crop_thresh)

        if license_text is not None:
            results[frame_nmr][car_id] = {
                'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                'license_plate': {
                    'bbox': [x1, y1, x2, y2],
                    'text': license_text,
                    'bbox_score': score,
                    'text_score': license_text_score
                }
            }

            cv2.putText(frame, license_text, (int(x1), int(y2) + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# === Save Output
cv2.imwrite('output_image.jpg', frame)
write_csv(results, 'test_image.csv')  # you can add tanggal='2025-06-22'
print("Hasil disimpan ke output_image.jpg dan test_image.csv")
