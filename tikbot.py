from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    format_type = request.form['format']
    file_ext = 'mp4' if format_type == 'mp4' else 'm4a'
    filename = f"{uuid.uuid4()}.{file_ext}"

    ydl_opts = {
        'format': 'best[ext=mp4][height<=360]' if format_type == 'mp4' else 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': filename,
        'quiet': True
    }

    def delayed_remove(path):
        time.sleep(10)
        if os.path.exists(path):
            os.remove(path)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    threading.Thread(target=delayed_remove, args=(filename,)).start()
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
