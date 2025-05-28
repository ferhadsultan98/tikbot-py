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
    ext = 'mp4' if format_type == 'mp4' else 'm4a'
    filename = f"{uuid.uuid4()}.{ext}"

    ydl_opts = {
        'outtmpl': filename,
        'quiet': True,
        'noplaylist': True,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]' if format_type == 'mp4' else 'bestaudio[ext=m4a]/bestaudio',
        'merge_output_format': None,
        'cookiefile': 'cookies.txt'
    }

    def delayed_remove(path):
        time.sleep(30)
        if os.path.exists(path):
            os.remove(path)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            if not os.path.exists(filename):
                return "Fayl tapılmadı – ola bilər ki, format dəstəklənmir."
    except Exception as e:
        return f"Yükləmə zamanı xəta baş verdi: {str(e)}"

    threading.Thread(target=delayed_remove, args=(filename,)).start()
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
