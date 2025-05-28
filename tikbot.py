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
    url = request.form['url']
    fmt = request.form['format']  # 'mp3' or 'mp4'
    ext = 'm4a' if fmt == 'mp3' else 'mp4'
    filename = f"{uuid.uuid4()}.{ext}"

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]' if fmt == 'mp3' else 'best[ext=mp4]',
        'outtmpl': filename,
        'quiet': True,
        'cookiefile': 'cookies.txt'
    }

    def remove_later(f):
        time.sleep(60)
        if os.path.exists(f):
            os.remove(f)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Hata oluştu: {e}"

    threading.Thread(target=remove_later, args=(filename,)).start()
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
