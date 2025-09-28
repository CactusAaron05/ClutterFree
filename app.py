from flask import Flask, render_template, request
import os
import shutil
import json

app = Flask(__name__)

PROJECT_NAME = "ClutterFree"
LOG_FILE_PATH = "report.log"

FILE_CATEGORIES = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    "Audio": ['.mp3', '.wav', '.aac', '.flac'],
    "Videos": ['.mp4', '.mkv', '.mov', '.wmv', '.flv'],
    "Archives": ['.zip', '.rar', '.tar', '.gz', '.7z'],
    "Scripts": ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c']
}

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def save_report(logs, files_moved):
    report_data = {
        "logs": logs,
        "files_moved": files_moved
    }
    with open(LOG_FILE_PATH, "w") as f:
        json.dump(report_data, f)

def load_report():
    if not os.path.exists(LOG_FILE_PATH):
        return {"logs": [], "files_moved": 0}
    with open(LOG_FILE_PATH, "r") as f:
        return json.load(f)

def organize_files(target_dir):
    files_moved = 0
    logs = []

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isfile(item_path):
            category = get_category(item)
            category_path = os.path.join(target_dir, category)
            create_folder_if_not_exists(category_path)

            dest_path = os.path.join(category_path, item)
            base, extension = os.path.splitext(item)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(category_path, f"{base}({counter}){extension}")
                counter += 1

            shutil.move(item_path, dest_path)
            logs.append(f"Moved: {item} --> {category}/")
            files_moved += 1

    save_report(logs, files_moved)
    return files_moved, logs

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    logs = []
    if request.method == 'POST':
        target_dir = request.form.get('directory').strip()
        if not os.path.isdir(target_dir):
            message = f"Invalid directory path. Please try again."
        else:
            files_moved, logs = organize_files(target_dir)
            message = f"{PROJECT_NAME} successfully organized {files_moved} files."
    return render_template('index.html', message=message, logs=logs, project_name=PROJECT_NAME)

@app.route('/report')
def report():
    report_data = load_report()
    return render_template('report.html', report=report_data.get("logs", []),
                           files_moved=report_data.get("files_moved", 0),
                           project_name=PROJECT_NAME)

@app.route('/help')
def help():
    help_text = f"""
    <h3>{PROJECT_NAME} Help</h3>
    <ul>
      <li>Enter the full path of the directory you want to organize.</li>
      <li>Click 'Start Organization' to move files into categorized folders.</li>
      <li>Supported categories: Images, Documents, Audio, Videos, Archives, Scripts.</li>
      <li>Ensure the directory path is correct and accessible.</li>
    </ul>
    """
    return render_template('help.html', help_text=help_text, project_name=PROJECT_NAME)

@app.route('/clear-report')
def clear_report():
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)
    return "Report cleared. <a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
