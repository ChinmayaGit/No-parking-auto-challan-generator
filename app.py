from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess
from videoprocess import change_frame_rate

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB limit for file size

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Counter for naming uploaded videos
video_count = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global video_count

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the file with a new name based on the counter
        video_count += 0.5
        filename = os.path.join(app.config['UPLOAD_FOLDER'], f"video_{video_count}.mp4")
        video_count += 0.5
        file.save(filename)
        filename2 = os.path.join(app.config['UPLOAD_FOLDER'], f"video_{video_count}.mp4")
        change_frame_rate(filename, filename2, frame_rate=5)
        # file.save(filename2)
        file_path = os.path.abspath(filename)
        os.remove(file_path)

        yolo_script_path = 'recognizer_plate.py'
        subprocess.run(['python', yolo_script_path], check=True)
        return render_template('index.html', filename=f"video_{video_count}.mp4")


from flask import send_file


@app.route('/download/licdet.csv')
def download_result():
    # Get the latest CSV file in the current directory
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]

    if not csv_files:
        raise FileNotFoundError("No CSV files found in the current directory.")

    latest_csv = max(csv_files, key=lambda x: os.path.getctime(x))
    return send_from_directory('.', latest_csv, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
