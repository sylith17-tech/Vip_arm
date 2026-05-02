import os
import requests
import yt_dlp
import threading
import logging
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS

# ==========================================
# [CENTRAL_INTELLIGENCE_CORE] - NODE: Kernel-0x0
# ==========================================

# إعداد نظام المراقبة الاستخباراتي
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [NODE_ID: Kernel-0x0] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.')
CORS(app)

# --- إعدادات الهوية والعمليات (Environment Variables) ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")

# مصفوفة البيانات الاستخباراتية للمطور
VIP_DATA = {
    "identity": {
        "alias": "VIP_ARM",
        "rank": "Lead Security Researcher",
        "node": "Kernel-0x0",
        "os_version": "VIP_ARM OS V6.0"
    },
    "platforms": {
        "facebook": "https://www.facebook.com/share/17BjmHpbUk/",
        "telegram_admin": "https://t.me/litharm"
    },
    "operational_unit": {
        "bot_username": "@MyVIP_2026_bot",
        "bot_link": "https://t.me/MyVIP_2026_bot",
        "status": "Operational",
        "uptime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

# ==========================================
# [UTILITY_ENGINES] - محركات الخدمات
# ==========================================

def get_gps_data(exif_data):
    """استخراج وتحويل إحداثيات GPS إلى روابط خرائط"""
    gps_info = {}
    if 'GPSInfo' in exif_data:
        for key in exif_data['GPSInfo'].keys():
            decode = GPSTAGS.get(key, key)
            gps_info[decode] = exif_data['GPSInfo'][key]
        
        # إذا وجدت إحداثيات، يمكن إضافة منطق تحويلها لرابط Maps هنا
        if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
            gps_info['map_link'] = "https://www.google.com/maps/search/?api=1&query=lat,lon"
    return gps_info

def transmit_intel_signal(subject, message):
    """إرسال إشارة مشفرة إلى قناة التلجرام في الخلفية"""
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
        logger.info(f"Signal {subject} transmitted to command center.")
    except Exception as e:
        logger.error(f"Signal transmission failed: {e}")

# ==========================================
# [API_RECON_ENDPOINTS] - مسارات النظام
# ==========================================

@app.route('/')
def main_node():
    """واجهة التحكم الرئيسية"""
    return render_template('index.html')

@app.route('/api/intel-profile')
def get_intel_profile():
    """تزويد الواجهة ببيانات المطور والبوت"""
    return jsonify(VIP_DATA)

@app.route('/api/status')
def node_status():
    """فحص حالة النظام"""
    return jsonify({
        "status": "Online",
        "encryption": "AES-256-Bit Ready",
        "active_node": "Kernel-0x0",
        "security_level": "Protocol 9"
    })

# --- جسر الإشارات (Signal Bridge) ---
@app.route('/send_message', methods=['POST'])
def handle_signal():
    data = request.json
    subject = data.get('subject', 'Web_Signal')
    message = data.get('message', 'No Data Provided')
    
    # المعالجة عبر خيط منفصل لسرعة الاستجابة
    threading.Thread(target=transmit_intel_signal, args=(subject, message)).start()
    return jsonify({"status": "transmitted", "tracking_id": os.urandom(4).hex()}), 202

# --- محرك الوسائط (Media Extraction) ---
@app.route('/api/download', methods=['POST'])
def media_engine():
    target_url = request.json.get('url')
    if not target_url: return jsonify({"error": "Empty Target"}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            transmit_intel_signal("Media_Recon", f"Extracted: {info.get('title')[:30]}...")
            return jsonify({
                "status": "success",
                "intel": {
                    "title": info.get('title'),
                    "duration": info.get('duration'),
                    "uploader": info.get('uploader'),
                    "dl_link": info.get('url')
                }
            })
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

# --- الماسح الأمني (Security Scanner) ---
@app.route('/api/scan', methods=['POST'])
def vulnerability_scanner():
    target = request.json.get('url')
    if not target.startswith('http'): target = 'https://' + target

    scan_report = {
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "security_headers": {},
        "risk_level": "Low"
    }

    try:
        response = requests.get(target, timeout=15, headers={'User-Agent': 'VIP-ARM-Recon/6.0'})
        headers = response.headers
        
        check_list = ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Frame-Options']
        missing_count = 0
        
        for h in check_list:
            status = "Found" if h in headers else "Missing"
            if status == "Missing": missing_count += 1
            scan_report["security_headers"][h] = status
            
        if missing_count > 1: scan_report["risk_level"] = "Critical"
        
        return jsonify(scan_report)
    except Exception as e:
        return jsonify({"error": "Host Unreachable", "details": str(e)}), 500

# --- التحليل الجنائي (Forensic Analysis) ---
@app.route('/api/exif', methods=['POST'])
def forensic_core():
    if 'image' not in request.files: return jsonify({"error": "No Payload"}), 400
    file = request.files['image']
    
    try:
        img = Image.open(file)
        raw_exif = img._getexif()
        
        if not raw_exif:
            return jsonify({"status": "clear", "message": "Zero Metadata Detected"})

        report = {}
        for tag_id, value in raw_exif.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == "GPSInfo":
                report["Geographic_Data"] = get_gps_data({"GPSInfo": value})
            else:
                report[tag_name] = str(value)

        return jsonify({"status": "extracted", "forensic_data": report})
    except Exception as e:
        return jsonify({"error": "Analysis Failed", "log": str(e)}), 500

# --- مدير الملفات الثابتة ---
@app.route('/<path:path>')
def router(path):
    """نظام توجيه ديناميكي لمنع أخطاء 404"""
    if os.path.exists(path):
        return send_from_directory('.', path)
    return render_template('index.html')

# ==========================================
# [CORE_BOOT_SEQUENCE]
# ==========================================

if __name__ == '__main__':
    # تهيئة السيرفر للعمل في بيئة السحاب (Render)
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"System Booting on Port {port}...")
    app.run(host='0.0.0.0', port=port, threaded=True)
