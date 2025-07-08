import csv
import numpy as np
from scipy.interpolate import interp1d
from datetime import datetime

def interpolate_bounding_boxes(data, tanggal=None):
    """
    Interpolates bounding boxes and adds violation detection metadata.

    Args:
        data (list): List of dict rows from the original CSV.
        tanggal (str): Date string in format 'YYYY-MM-DD'. If None, uses current date.

    Returns:
        list: List of dicts with interpolated + metadata.
    """
    if tanggal is None:
        tanggal = datetime.now().strftime('%Y-%m-%d')
    tanggal_int = int(tanggal.split('-')[2])

    frame_numbers = np.array([int(row['frame_nmr']) for row in data])
    car_ids = np.array([int(float(row['car_id'])) for row in data])
    car_bboxes = np.array([list(map(float, row['car_bbox'][1:-1].split())) for row in data])
    license_plate_bboxes = np.array([list(map(float, row['license_plate_bbox'][1:-1].split())) for row in data])

    interpolated_data = []
    unique_car_ids = np.unique(car_ids)
    for car_id in unique_car_ids:
        frame_numbers_ = [p['frame_nmr'] for p in data if int(float(p['car_id'])) == int(float(car_id))]

        car_mask = car_ids == car_id
        car_frame_numbers = frame_numbers[car_mask]
        car_bboxes_interpolated = []
        license_plate_bboxes_interpolated = []

        first_frame_number = car_frame_numbers[0]

        for i in range(len(car_bboxes[car_mask])):
            frame_number = car_frame_numbers[i]
            car_bbox = car_bboxes[car_mask][i]
            license_plate_bbox = license_plate_bboxes[car_mask][i]

            if i > 0:
                prev_frame_number = car_frame_numbers[i - 1]
                prev_car_bbox = car_bboxes_interpolated[-1]
                prev_license_plate_bbox = license_plate_bboxes_interpolated[-1]

                if frame_number - prev_frame_number > 1:
                    frames_gap = frame_number - prev_frame_number
                    x = np.array([prev_frame_number, frame_number])
                    x_new = np.linspace(prev_frame_number, frame_number, num=frames_gap, endpoint=False)
                    car_interp = interp1d(x, np.vstack((prev_car_bbox, car_bbox)), axis=0, kind='linear')
                    lp_interp = interp1d(x, np.vstack((prev_license_plate_bbox, license_plate_bbox)), axis=0, kind='linear')

                    car_bboxes_interpolated.extend(car_interp(x_new)[1:])
                    license_plate_bboxes_interpolated.extend(lp_interp(x_new)[1:])

            car_bboxes_interpolated.append(car_bbox)
            license_plate_bboxes_interpolated.append(license_plate_bbox)

        for i in range(len(car_bboxes_interpolated)):
            frame_number = first_frame_number + i
            row = {}
            row['frame_nmr'] = str(frame_number)
            row['car_id'] = str(car_id)
            row['car_bbox'] = '[{}]'.format(' '.join(map(str, car_bboxes_interpolated[i])))
            row['license_plate_bbox'] = '[{}]'.format(' '.join(map(str, license_plate_bboxes_interpolated[i])))

            if str(frame_number) not in frame_numbers_:
                row['license_plate_bbox_score'] = '0'
                row['license_number'] = '0'
                row['license_number_score'] = '0'
                row['ganjil_genap'] = 'tidak diketahui'
                row['tanggal'] = tanggal
                row['keterangan'] = 'Tidak diketahui'
            else:
                original_row = next(p for p in data if int(p['frame_nmr']) == frame_number and int(float(p['car_id'])) == int(float(car_id)))
                row['license_plate_bbox_score'] = original_row.get('license_plate_bbox_score', '0')
                row['license_number'] = original_row.get('license_number', '0')
                row['license_number_score'] = original_row.get('license_number_score', '0')
                row['tanggal'] = original_row.get('tanggal', tanggal)

                last_digit = next((c for c in reversed(row['license_number']) if c.isdigit()), None)
                if last_digit:
                    row['ganjil_genap'] = 'ganjil' if int(last_digit) % 2 == 1 else 'genap'
                    row['keterangan'] = 'Pelanggaran' if (int(last_digit) % 2) != (tanggal_int % 2) else 'Aman'
                else:
                    row['ganjil_genap'] = 'tidak diketahui'
                    row['keterangan'] = 'Tidak diketahui'

            interpolated_data.append(row)

    return interpolated_data


# === Eksekusi utama
with open('test_image.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

interpolated_data = interpolate_bounding_boxes(data)

header = ['frame_nmr', 'car_id', 'car_bbox', 'license_plate_bbox',
          'license_plate_bbox_score', 'license_number', 'license_number_score',
          'ganjil_genap', 'tanggal', 'keterangan']

with open('test_interpolated.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(interpolated_data)

os.makedirs('csv', exist_ok=True)
with open('csv/data_pelanggaran.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['tanggal', 'nomor_plat', 'ganjil_genap', 'keterangan'])
    for row in interpolated_data:
        writer.writerow([
            row['tanggal'],
            row['license_number'],
            row['ganjil_genap'],
            row['keterangan']
        ])
