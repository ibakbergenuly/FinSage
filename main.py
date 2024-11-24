import webview
import threading
from app import app, start_file_watcher, os

def start_flask():
    os.makedirs("uploads", exist_ok=True)
    observer = start_file_watcher()
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()
    
    # Create a native window
    webview.create_window(
        'FinSage', 
        'http://127.0.0.1:5000',
        width=1200,
        height=800,
        resizable=True,
    )
    webview.start()
