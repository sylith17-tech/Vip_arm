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

# ==========================================
# [CENTRAL_INTELLIGENCE_CORE] - NODE: Kernel-0x0
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [NODE_ID: Kernel-0x0] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.')
CORS(app)

# --- إعدادات الهوية (Environment Variables) ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")

VIP_DATA = {
    "identity": {
        "alias": "VIP_ARM",
        "rank": "Lead Security Researcher",
        "node": "Kernel-0x0",
        "os_version": "VIP_ARM OS V6.0"
    },
    "operational_unit": {
        "bot_username": "@MyVIP_2026_bot",
        "status": "Operational",
        "uptime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

# ==========================================
# [UTILITY_ENGINES] - محركات الخدمات
# ==========================================

def get_gps_data(exif_data):
    gps_info = {}
    if 'GPSInfo' in exif_data:
        for key in exif_data['GPSInfo'].keys():
            decode = GPSTAGS.get(key, key)
            gps_info[decode] = exif_data['GPSInfo'][key]
    return gps_info

def transmit_intel_signal(subject, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    payload = (
        f"🚨 **[VIP_INTEL_SIGNAL]**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🖥 **Node:** Kernel-0x0\n"
        f"⏰ **Time:** {timestamp}\n"
        f"📂 **Subject:** {subject}\n"
        f"📥 **Data:** {message}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🛡 **Control:** @MyVIP_2026_bot"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": payload, "parse_mode": "Markdown"})
    except Exception as e:
        logger.error(f"Signal transmission failed: {e}")

# ==========================================
# [API_RECON_ENDPOINTS] - مسارات النظام
# ==========================================

@app.route('/')
def main_node():
    return render_template('index.html')

@app.route('/api/intel-profile')
def get_intel_profile():
    return jsonify(VIP_DATA)

@app.route('/send_message', methods=['POST'])
def handle_signal():
    data = request.json
    subject = data.get('subject', 'Web_Signal')
    message = data.get('message', 'No Data Provided')
    threading.Thread(target=transmit_intel_signal, args=(subject, message)).start()
    return jsonify({"status": "transmitted"}), 202

@app.route('/api/download', methods=['POST'])
def media_engine():
    target_url = request.json.get('url')
    if not target_url: return jsonify({"error": "Empty Target"}), 400

    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            return jsonify({
                "status": "success",
                "intel": { # التأكد من أن المفتاح هو intel لتجنب undefined في JS
                    "title": info.get('title', 'Unknown'),
                    "duration": info.get('duration', 0),
                    "uploader": info.get('uploader', 'Unknown'),
                    "dl_link": info.get('url'),
                    "thumbnail": info.get('thumbnail')
                }
            })
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

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

# --- نظام التوجيه الذكي (إصلاح تضارب المسارات) ---
@app.route('/<path:path>')
def static_proxy(path):
    # إذا كان الملف موجوداً فعلياً في المجلد، قم بخدمته
    if os.path.exists(os.path.join(app.root_path, path)):
        return send_from_directory('.', path)
    # إذا كان المسار يبدأ بـ api ولم يتم التعرف عليه، أعطِ 404 بدلاً من إعادة تحميل index
    if path.startswith('api/'):
        return jsonify({"error": "Endpoint Not Found"}), 404
    # في حال فشل كل ما سبق، عد للقائمة الرئيسية
    return render_template('index.html')

# ==========================================
# [CORE_BOOT_SEQUENCE]
# ==========================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # التشغيل بوضع host='0.0.0.0' ضروري لـ Render
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)
