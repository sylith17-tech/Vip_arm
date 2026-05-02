import os
import requests
import yt_dlp
import threading
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# [CENTRAL_INTELLIGENCE_CORE] - NODE: Kernel-0x0
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [NODE_ID: Kernel-0x0] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.', static_folder='.')
# تكوين CORS للسماح بجميع النطاقات (ضروري لـ Render)
CORS(app, resources={r"/*": {"origins": "*"}})

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")

VIP_DATA = {
    "identity": {"alias": "VIP_ARM", "rank": "Lead Security Researcher", "node": "Kernel-0x0"},
    "operational_unit": {"bot_username": "@MyVIP_2026_bot", "status": "Operational"}
}

# --- محرك استخراج الميديا المطور ---
def get_media_info(target_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            if not info: return None
            return {
                "title": info.get('title', 'No Title Found'),
                "duration": info.get('duration', 0),
                "uploader": info.get('uploader', 'Unknown Source'),
                "dl_link": info.get('url'),
                "thumbnail": info.get('thumbnail', 'https://via.placeholder.com/150'),
                "platform": info.get('extractor', 'web')
            }
    except Exception as e:
        logger.error(f"yt-dlp Error: {str(e)}")
        return None

# --- المسارات (Endpoints) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def media_engine():
    data = request.json
    target_url = data.get('url')
    if not target_url:
        return jsonify({"status": "failed", "error": "URL is required"}), 400

    logger.info(f"Processing URL: {target_url}")
    intel = get_media_info(target_url)
    
    if intel:
        return jsonify({"status": "success", "intel": intel})
    else:
        return jsonify({"status": "failed", "error": "Could not extract media data. Platform might be restricted."}), 500

@app.route('/api/exif', methods=['POST'])
def forensic_core():
    if 'image' not in request.files: return jsonify({"error": "No Payload"}), 400
    file = request.files['image']
    try:
        img = Image.open(file)
        raw_exif = img._getexif()
        if not raw_exif: return jsonify({"status": "clear", "message": "Zero Metadata"})
        report = {TAGS.get(tid, tid): str(val) for tid, val in raw_exif.items()}
        return jsonify({"status": "extracted", "forensic_data": report})
    except Exception as e:
        return jsonify({"error": "Analysis Failed", "log": str(e)}), 500

# لضمان عمل الملفات الثابتة (JS/CSS) بشكل صحيح على Render
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Render يستخدم المتغير PORT تلقائياً
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
