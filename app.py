import os
import requests
import yt_dlp
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
from PIL.ExifTags import TAGS

app = Flask(__name__, template_folder='.')
CORS(app)

# 1. تشغيل الصفحات الأساسية
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return render_template('index.html')

# 2. أداة التحميل الحقيقية لجميع المواقع (TikTok, Insta, YT, etc.)
@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_direct_url = info.get('url')
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail')
            
            return jsonify({
                "status": "success",
                "title": title,
                "download_link": video_direct_url,
                "thumbnail": thumbnail
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 3. أداة EXIF Forensic (حقيقية)
@app.route('/api/exif', methods=['POST'])
def extract_exif():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files['image']
    try:
        img = Image.open(file)
        info = img._getexif()
        exif_table = {}
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_table[decoded] = str(value)
            return jsonify({"status": "success", "data": exif_table})
        return jsonify({"status": "warning", "message": "No EXIF data found."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 4. أداة Scanner (حقيقية)
@app.route('/api/scan', methods=['POST'])
def scan_website():
    data = request.json
    target_url = data.get('url')
    if not target_url.startswith('http'): target_url = 'https://' + target_url
    try:
        response = requests.get(target_url, timeout=10)
        headers = dict(response.headers)
        return jsonify({
            "status": "success",
            "results": {
                "status_code": response.status_code,
                "server": headers.get('Server', 'Unknown'),
                "security": "Headers Analyzed Successfully"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
