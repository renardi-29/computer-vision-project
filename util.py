import string
import easyocr
from datetime import datetime

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0', 'I': '1', 'J': '3', 'A': '4', 'G': '6', 'S': '5'}
dict_int_to_char = {'0': 'O', '1': 'I', '3': 'J', '4': 'A', '6': 'G', '5': 'S'}


def write_csv(results, output_path, tanggal=None):
    """
    Write the results to a CSV file with additional columns for date and odd/even violation.

    Args:
        results (dict): Dictionary containing detection results.
        output_path (str): Path to the output CSV file.
        tanggal (str): Optional. Date in format 'YYYY-MM-DD'. If None, use current date.
    """
    if tanggal is None:
        tanggal = datetime.now().strftime('%Y-%m-%d')

    tanggal_int = int(tanggal.split('-')[2])  # extract day part

    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(
            'frame_nmr', 'car_id', 'car_bbox',
            'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
            'license_number_score', 'ganjil_genap', 'tanggal', 'keterangan'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                if 'car' in results[frame_nmr][car_id] and \
                   'license_plate' in results[frame_nmr][car_id] and \
                   'text' in results[frame_nmr][car_id]['license_plate']:

                    license_number = results[frame_nmr][car_id]['license_plate']['text']
                    last_digit = next((c for c in reversed(license_number) if c.isdigit()), None)

                    if last_digit:
                        ganjil_genap = 'ganjil' if int(last_digit) % 2 == 1 else 'genap'
                    else:
                        ganjil_genap = 'tidak diketahui'

                    if last_digit and ganjil_genap != 'tidak diketahui':
                        if (int(last_digit) % 2) != (tanggal_int % 2):
                            keterangan = 'Pelanggaran'
                        else:
                            keterangan = 'Aman'
                    else:
                        keterangan = 'Tidak diketahui'

                    f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(
                        frame_nmr,
                        car_id,
                        '[{} {} {} {}]'.format(*results[frame_nmr][car_id]['car']['bbox']),
                        '[{} {} {} {}]'.format(*results[frame_nmr][car_id]['license_plate']['bbox']),
                        results[frame_nmr][car_id]['license_plate']['bbox_score'],
                        license_number,
                        results[frame_nmr][car_id]['license_plate']['text_score'],
                        ganjil_genap,
                        tanggal,
                        keterangan
                    ))
        f.close()


def license_complies_format(text):
    """
    Check if the license plate text complies with the expected format.

    Args:
        text (str): Detected license plate text.

    Returns:
        bool: True if format matches, False otherwise.
    """
    if len(text) != 7:
        return False
    return (
        (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char) and
        (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char) and
        (text[2] in string.digits or text[2] in dict_char_to_int) and
        (text[3] in string.digits or text[3] in dict_char_to_int) and
        (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char) and
        (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char) and
        (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char)
    )


def format_license(text):
    """
    Format the license plate string by converting potentially misread characters.

    Args:
        text (str): Raw license plate text.

    Returns:
        str: Formatted license plate text.
    """
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char,
               5: dict_int_to_char, 6: dict_int_to_char, 2: dict_char_to_int, 3: dict_char_to_int}
    for j in range(7):
        if text[j] in mapping[j]:
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]
    return license_plate_


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from cropped image.

    Args:
        license_plate_crop (numpy.ndarray): Cropped license plate image.

    Returns:
        tuple: (formatted_text, confidence_score) or (None, None)
    """
    detections = reader.readtext(license_plate_crop)
    for bbox, text, score in detections:
        text = text.upper().replace(' ', '')
        if license_complies_format(text):
            return format_license(text), score
    return None, None


def get_car(license_plate, vehicle_track_ids):
    """
    Retrieve the vehicle coordinates and ID based on the license plate coordinates.

    Args:
        license_plate (tuple): Tuple of (x1, y1, x2, y2, score, class_id) from license plate detector.
        vehicle_track_ids (list): List of tracked vehicles [x1, y1, x2, y2, id].

    Returns:
        tuple: (x1, y1, x2, y2, car_id) if found, else -1s.
    """
    x1, y1, x2, y2, score, class_id = license_plate
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]
        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            return vehicle_track_ids[j]
    return -1, -1, -1, -1, -1
