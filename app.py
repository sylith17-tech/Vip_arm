import os
import requests
import yt_dlp
import threading
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS

# --- إعداد نظام المراقبة (Intel Logging) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] Node: Kernel-0x0 - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.')
CORS(app)

# --- إعدادات القنوات المشفرة ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")

DEV_INFO = {
    "alias": "VIP_ARM",
    "node": "Kernel-0x0",
    "platforms": {
        "facebook": "https://www.facebook.com/share/17BjmHpbUk/",
        "telegram": "https://t.me/litharm"
    },
    "intel_unit": {
        "bot": "@MyVIP_2026_bot",
        "type": "Advanced Intelligence & Recon Bot",
        "status": "Operational"
    }
}

# --- وظائف مساعدة (Utility Functions) ---
def get_gps_info(exif_data):
    """استخراج إحداثيات GPS من بيانات EXIF"""
    gps_info = {}
    if 'GPSInfo' in exif_data:
        for key in exif_data['GPSInfo'].keys():
            decode = GPSTAGS.get(key, key)
            gps_info[decode] = exif_data['GPSInfo'][key]
    return gps_info

# --- 1. واجهة النظام ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def system_status():
    return jsonify({"node": "Kernel-0x0", "status": "Online", "security_level": "Maximum"})

# --- 2. جسر الإشارات (Signal Bridge) ---
@app.route('/send_message', methods=['POST'])
def send_signal():
    data = request.json
    def transmit():
        payload = (
            f"📡 **[NEW_INTEL_SIGNAL]**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🖥 **Node:** Kernel-0x0\n"
            f"📂 **Type:** {data.get('subject', 'General')}\n"
            f"📥 **Data:** {data.get('message', 'N/A')}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🛡 @MyVIP_2026_bot | **SECURE**"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": payload, "parse_mode": "Markdown"})
            logger.info("Signal transmitted successfully.")
        except Exception as e:
            logger.error(f"Transmission failed: {e}")

    # تشغيل في خلفية النظام لعدم تأخير الاستجابة
    threading.Thread(target=transmit).start()
    return jsonify({"status": "queued", "node": "Kernel-0x0"}), 202

# --- 3. محرك التحميل الاستخباراتي (Media Recon) ---
@app.route('/api/download', methods=['POST'])
def download_engine():
    video_url = request.json.get('url')
    if not video_url: return jsonify({"error": "Target missing"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'extract_flat': True # تسريع العملية بجلب الروابط فقط
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "status": "extracted",
                "title": info.get('title'),
                "source": info.get('extractor'),
                "url": info.get('url') or info.get('webpage_url')
            })
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

# --- 4. فحص الثغرات المتقدم (Vulnerability Analysis) ---
@app.route('/api/scan', methods=['POST'])
def security_audit():
    target = request.json.get('url')
    if not target.startswith('http'): target = 'https://' + target

    audit_results = {
        "target": target,
        "firewall_detected": False,
        "vulnerabilities": []
    }

    try:
        headers = {'User-Agent': 'Kernel-0x0-Intel-Bot/5.3'}
        response = requests.get(target, headers=headers, timeout=12)
        
        # كشف الجدران النارية
        server = response.headers.get('Server', '').lower()
        if 'cloudflare' in server or 'sucuri' in server:
            audit_results["firewall_detected"] = True

        # فحص بروتوكولات الأمان
        if 'Strict-Transport-Security' not in response.headers:
            audit_results["vulnerabilities"].append("Missing HSTS (MITM Risk)")
        
        return jsonify(audit_results)
    except Exception as e:
        return jsonify({"error": "Target unreachable"}), 500

# --- 5. تحليل الصور الجنائي (Forensic Analysis) ---
@app.route('/api/exif', methods=['POST'])
def forensic_analysis():
    if 'image' not in request.files: return jsonify({"error": "No payload"}), 400
    file = request.files['image']
    
    try:
        img = Image.open(file)
        raw_exif = img._getexif()
        
        if not raw_exif:
            return jsonify({"status": "clean", "message": "No metadata found"})

        decoded_exif = {}
        for tag, value in raw_exif.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == "GPSInfo":
                decoded_exif["GPS_Location"] = get_gps_info({"GPSInfo": value})
            else:
                decoded_exif[tag_name] = str(value)

        return jsonify({"status": "extracted", "metadata": decoded_exif})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # تشغيل السيرفر مع دعم الـ Multithreading
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
