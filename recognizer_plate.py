import os
import csv
import subprocess
from paddleocr import PaddleOCR, draw_ocr
from text_processing import clean_text, contains_license_plate_format
import shutil

# Automatically run the YOLO script
yolo_script_path = 'load_yolo_model.py'
subprocess.run(['python', yolo_script_path], check=True)

# Continue with PaddleOCR logic
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Extract numerical part from folder names
import re


# Extract numerical part from folder names
def extract_numeric_part(folder_name):
    match = re.search(r'\d+', folder_name)
    return int(match.group()) if match else float('-inf')  # Use negative infinity for folders without a numeric part


# Find the latest predict folder
predict_folders = [folder for folder in os.listdir('runs/detect') if folder.startswith('predict')]
latest_predict_folder = max(predict_folders, key=extract_numeric_part, default=None)

if latest_predict_folder:
    input_directory = f'runs/detect/{latest_predict_folder}/crops/0'
    base_output_csv_name = 'licdet.csv'
    output_csv_path = base_output_csv_name
    file_counter = 1

    while os.path.exists(output_csv_path):
        output_csv_path = f'licdet_{file_counter}.csv'
        file_counter += 1

    unique_license_plates = set()

    with open(output_csv_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        for filename in os.listdir(input_directory):
            item_path = os.path.join(input_directory, filename)

            result = ocr.ocr(item_path, cls=True)

            if result and result[0]:
                # Concatenate all recognized texts dynamically
                recognized_texts = ''
                for line in result:
                    for word_info in line:
                        recognized_texts += word_info[1][0]

                # Clean the recognized text and keep only alphanumeric characters
                cleaned_text = clean_text(recognized_texts)

                # Check if the cleaned text is not empty and contains the specified format
                if cleaned_text and contains_license_plate_format(
                        cleaned_text) and cleaned_text not in unique_license_plates:
                    unique_license_plates.add(cleaned_text)

                    # Write to CSV file
                    csv_writer.writerow([cleaned_text])

if latest_predict_folder:
    folder_path = os.path.join('runs/detect', latest_predict_folder)
    shutil.rmtree(folder_path)
