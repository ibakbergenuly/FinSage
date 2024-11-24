import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from flask import Flask, render_template, Response
from mistral_service import MistralService
import markdown
import json

app = Flask(__name__)
WATCH_DIRECTORY = "uploads"
ALLOWED_EXTENSION = ".finsage"

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        self.mistral = MistralService()
        self.latest_response = None
        self.processing = False
        self.current_file = None

    def read_file_with_retry(self, filepath, max_attempts=5):
        for attempt in range(max_attempts):
            try:
                time.sleep(1)
                with open(filepath, 'r') as file:
                    return file.read()
            except PermissionError:
                continue
        return None

    def analyze_current_file(self):
        if self.current_file:
            self.processing = True
            text = self.read_file_with_retry(self.current_file)
            if text:
                self.latest_response = self.mistral.analyze_file(text)
            self.processing = False

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(ALLOWED_EXTENSION):
            self.current_file = event.src_path
            self.analyze_current_file()

    def reset_response(self):
        self.latest_response = None

file_handler = FileHandler()

@app.route('/retry')
def retry():
    file_handler.analyze_current_file()
    return '', 204

@app.route('/')
def home():
    file_handler.reset_response()  # Reset response on page load
    return render_template('index.html')

@app.route('/stream')
def stream():
    def event_stream():
        previous_response = None
        previous_processing = False
        while True:
            if file_handler.processing != previous_processing:
                previous_processing = file_handler.processing
                yield f"data: {json.dumps({'processing': file_handler.processing})}\n\n"
                
            if file_handler.latest_response != previous_response:
                previous_response = file_handler.latest_response
                if previous_response:
                    html_content = markdown.markdown(previous_response, extensions=['tables'])
                    yield f"data: {json.dumps({'response': html_content})}\n\n"
            time.sleep(1)
    
    return Response(event_stream(), mimetype="text/event-stream")
def start_file_watcher():
    observer = Observer()
    observer.schedule(file_handler, WATCH_DIRECTORY, recursive=False)
    observer.start()
    return observer

if __name__ == "__main__":
    os.makedirs(WATCH_DIRECTORY, exist_ok=True)
    observer = start_file_watcher()
    
    try:
        app.run(debug=True)
    finally:
        observer.stop()
        observer.join()
