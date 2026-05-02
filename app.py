import os
import yt_dlp
import logging
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, after_this_request
from flask_cors import CORS
from PIL import Image
from PIL.ExifTags import TAGS

# [CENTRAL_INTELLIGENCE_CORE] - NODE: Kernel-0x0
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [NODE_ID: Kernel-0x0] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app, resources={r"/*": {"origins": "*"}})

# تكوين المسارات
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# --- محرك التحميل والدمج المطور ---
def download_media(target_url):
    unique_id = str(uuid.uuid4())[:8]
    # قالب اسم الملف: downloads/filename.ext
    out_tmpl = os.path.join(DOWNLOAD_FOLDER, f'VIP_ARM_{unique_id}_%(title)s.%(ext)s')
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', # الدمج باستخدام ffmpeg
        'outtmpl': out_tmpl,
        'quiet': False,
        'no_warnings': False,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'restrictfilenames': True, # لتجنب المشاكل مع الأسماء العربية أو الرموز
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=True)
            file_path = ydl.prepare_filename(info)
            
            # في حال تم تغيير الامتداد بعد الدمج (مثلاً من mkv إلى mp4)
            actual_filename = file_path
            if not os.path.exists(file_path):
                # بحث بسيط عن الملف في المجلد إذا اختلف الامتداد
                base = os.path.splitext(file_path)[0]
                for f in os.listdir(DOWNLOAD_FOLDER):
                    if f.startswith(os.path.basename(base)):
                        actual_filename = os.path.join(DOWNLOAD_FOLDER, f)
                        break

            return {
                "status": "success",
                "file_path": actual_filename,
                "title": info.get('title', 'video'),
                "filename": os.path.basename(actual_filename)
            }
    except Exception as e:
        logger.error(f"Download Core Error: {str(e)}")
        return {"status": "failed", "error": str(e)}

# --- المسارات (Endpoints) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def handle_download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    logger.info(f"Initiating Download Task for: {url}")
    result = download_media(url)

    if result["status"] == "success":
        file_path = result["file_path"]
        
        # وظيفة لحذف الملف بعد إرساله للمستخدم لتوفير المساحة
        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleanup: Removed temporary file {file_path}")
            except Exception as e:
                logger.error(f"Cleanup Error: {e}")
            return response

        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"status": "failed", "error": result["error"]}), 500

@app.route('/api/info', methods=['POST'])
def handle_info():
    # هذا المسار فقط لعرض المعلومات قبل التحميل (اختياري)
    data = request.json
    url = data.get('url')
    ydl_opts = {'quiet': True, 'nocheckcertificate': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return jsonify({
            "title": info.get('title'),
            "thumbnail": info.get('thumbnail'),
            "duration": info.get('duration')
        })

@app.route('/api/exif', methods=['POST'])
def forensic_core():
    if 'image' not in request.files: return jsonify({"error": "No Payload"}), 400
    file = request.files['image']
    try:
        img = Image.open(file)
        raw_exif = img._getexif()
        if not raw_exif: return jsonify({"status": "clear", "message": "Zero Metadata"})
        report = {TAGS.get(tid, tid): str(val) for tid, val in raw_exif.items() if not isinstance(val, bytes)}
        return jsonify({"status": "extracted", "forensic_data": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Kernel-0x0 Deploying on Port: {port}")
    app.run(host='0.0.0.0', port=port)
