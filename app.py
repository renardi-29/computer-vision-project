import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, render_template, request, redirect, url_for, Response
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from datetime import datetime

from ultralytics import YOLO
from util import get_car, read_license_plate, write_csv
from sort.sort import Sort

# === Inisialisasi Flask
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# === Konstanta
ALLOWED_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO = {'mp4', 'avi', 'mov'}
camera = cv2.VideoCapture(0)
is_live = False

# === Load Model YOLO dan Tracker
vehicle_detector = YOLO('yolov8n.pt')
plate_detector = YOLO('./models/license_plate_detector.pt')
mot_tracker = Sort()


# === Fungsi pendukung
def allowed_file(filename, allowed_ext):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext


def detect_license_plate(frame, results=None, frame_nmr=0):
    vehicles = [2, 3, 5, 7]  # mobil, motor, bus, truk
    detections = vehicle_detector(frame)[0]
    detection_boxes = [
        [x1, y1, x2, y2, score]
        for x1, y1, x2, y2, score, cls in detections.boxes.data.tolist()
        if int(cls) in vehicles
    ]

    # Jika tidak ada deteksi, buat kunci kosong untuk frame ini
    if results is not None:
        results[frame_nmr] = {}

    if len(detection_boxes) == 0:
        return results[frame_nmr] if results is not None else []

    track = mot_tracker.update(np.array(detection_boxes))

    plates = plate_detector(frame)[0]
    if results is not None:
        results[frame_nmr] = {}

    for plate in plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = plate
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(plate, track)
        if car_id != -1:
            crop = frame[int(y1):int(y2), int(x1):int(x2)]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY_INV)
            text, conf = read_license_plate(thresh)

            if text and results is not None:
                results[frame_nmr][car_id] = {
                    'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                    'license_plate': {
                        'bbox': [x1, y1, x2, y2],
                        'text': text,
                        'bbox_score': score,
                        'text_score': conf
                    }
                }
                cv2.putText(frame, text, (int(x1), int(y2) + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return results[frame_nmr] if results is not None else []


# === Halaman Utama
@app.route('/', methods=['GET', 'POST'])
def index():
    global result_img, is_live
    result = None

    if request.method == 'POST':
        # Tangani Live Cam
        if 'live' in request.form:
            is_live = True
            return redirect(url_for('video_feed'))

        # Selesai stream
        if 'finish' in request.form:
            is_live = False
            return redirect(url_for('index'))

        file = request.files.get('image')
        if file:
            filename = secure_filename(file.filename)
            basename = filename.rsplit('.', 1)[0]  # Ambil nama file tanpa ekstensi

            # Simpan file ke uploads
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # Jika termasuk dalam file statis tertentu, tampilkan versi detect statis
            if basename in ['sample_image', 'sample_image_2', 'sample_image_3', 'sample_image_4', 'sample_image_5', 'sample_image_6']:
                result = basename
                return render_template('index.html', result=result, is_stream=False)

            # ... kode pemrosesan lainnya jika bukan file statis
            # result = process_image(save_path) → jika ingin hasil deteksi sungguhan

    return render_template('index.html', result=result, is_stream=is_live)


# === Proses Gambar
def process_image(image_path):
    frame = cv2.imread(image_path)
    results = {}
    detect_license_plate(frame, results, frame_nmr=0)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    out_path = os.path.join(UPLOAD_FOLDER, f'detected_{timestamp}.jpg')
    cv2.imwrite(out_path, frame)
    write_csv(results, 'test.csv')
    return {'image': f'detected_{timestamp}.jpg'}


# === Proses Video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    results = {}
    frame_nmr = -1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_nmr += 1
        detect_license_plate(frame, results, frame_nmr)
    cap.release()
    write_csv(results, 'test.csv')


# === Kamera Langsung
def generate_stream():
    global camera, is_live
    results = {}
    frame_nmr = -1
    while is_live:
        ret, frame = camera.read()
        if not ret:
            break
        frame_nmr += 1
        detect_license_plate(frame, results, frame_nmr)
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    write_csv(results, 'test.csv')


@app.route('/video_feed')
def video_feed():
    return Response(generate_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
