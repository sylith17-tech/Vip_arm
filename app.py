import os
import yt_dlp
import logging
import uuid
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from PIL import Image
from PIL.ExifTags import TAGS
# التوافق مع MoviePy 2.2.1 - تصحيح الاستيراد للمؤثرات
from moviepy import VideoFileClip
import moviepy.video.fx.all as vfx
from gtts import gTTS

# [CENTRAL_INTELLIGENCE_CORE] - NODE: Kernel-0x0
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [NODE_ID: Kernel-0x0] - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
STUDIO_FOLDER = os.path.join(os.getcwd(), 'studio_exports') 
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads') 

for folder in [DOWNLOAD_FOLDER, STUDIO_FOLDER, UPLOAD_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# وظيفة مساعدة لتنسيق حجم الملفات
def format_size(bytes):
    if not bytes: return "--"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024: return f"{bytes:.1f} {unit}"
        bytes /= 1024

def get_ydl_opts(custom_out=None):
    return {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': custom_out or os.path.join(DOWNLOAD_FOLDER, 'VIP_ARM_%(id)s.%(ext)s'),
        'nocheckcertificate': True,
        'quiet': True
    }

# --- ميزات المعالجة المتقدمة (AI Core) ---
def create_shorts(input_path):
    output_path = input_path.replace(".mp4", "_SHORTS.mp4")
    with VideoFileClip(input_path) as video:
        duration = min(video.duration, 60)
        clip = video.subclip(0, duration)
        w, h = clip.size
        target_ratio = 9/16
        target_w = h * target_ratio
        # تصحيح MoviePy 2.x: استخدام fx لتطبيق الـ Crop
        final_clip = clip.fx(vfx.crop, x_center=w/2, width=target_w)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

def dub_video(input_path, lang='ar'):
    output_path = input_path.replace(".mp4", "_DUBBED.mp4")
    temp_audio = f"temp_{uuid.uuid4()}.mp3"
    with VideoFileClip(input_path) as video:
        tts = gTTS(text="تمت المعالجة بواسطة محرك VIP_ARM", lang=lang)
        tts.save(temp_audio)
        # تصحيح MoviePy 2.x: تغيير set_audio إلى with_audio
        audio_clip = VideoFileClip(temp_audio).audio
        final_video = video.with_audio(audio_clip)
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return output_path

# --- إدارة المسارات (Routing Control) ---

@app.route('/')
def index():
    return render_template('index.html')

# مسار خاص بواجهة الاستوديو
@app.route('/studio')
def studio_page():
    return render_template('studio.html')

# --- [FIXED] مسار الرفع المخصص ---
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('image') or request.files.get('file')
    if not file:
        return jsonify({"error": "No Payload"}), 400

    filename = f"VIP_{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # تصحيح الرابط ليعود بمسار نسبي للمتصفح
    return jsonify({
        "status": "success",
        "url": f"/uploads/{filename}",
        "filename": filename
    })

@app.route('/<page>')
def serve_pages(page):
    # حماية المجلدات من التداخل مع المسارات العامة
    if os.path.exists(page) and not page.endswith('.html'):
        return send_file(page)
    if page.endswith('.html'): return render_template(page)
    if os.path.exists(f"{page}.html"): return render_template(f"{page}.html")
    return render_template('index.html'), 404

# --- API Endpoints ---

@app.route('/api/download', methods=['POST'])
@app.route('/api/process', methods=['POST'])
def unified_handler():
    data = request.json
    url = data.get('url')
    mode = data.get('mode')
    
    # تهيئة المسارات لتجنب أخطاء Cleanup
    raw_path = None
    final_path = None

    if not url:
        return jsonify({"status": "failed", "message": "No URL provided"}), 400

    try:
        if not mode:
            ydl_opts = {'quiet': True, 'nocheckcertificate': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = []
                for f in info.get('formats', [])[-8:]:
                    if f.get('url'):
                        formats.append({
                            "ext": f.get('ext', 'mp4'),
                            "resolution": f.get('resolution', 'N/A'),
                            "filesize": format_size(f.get('filesize') or f.get('filesize_approx')),
                            "url": f.get('url'),
                            "vcodec": f.get('vcodec', 'none')
                        })
                return jsonify({
                    "status": "success",
                    "title": info.get('title', 'Media Content'),
                    "thumbnail": info.get('thumbnail', ''),
                    "uploader": info.get('uploader', 'VIP_ARM_SOURCE'),
                    "duration": f"{int(info.get('duration', 0))//60}:{int(info.get('duration', 0))%60:02d}",
                    "formats": formats[::-1]
                })
        else:
            with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
                info = ydl.extract_info(url, download=True)
                raw_path = ydl.prepare_filename(info)

            if mode == 'shorts':
                final_path = create_shorts(raw_path)
            elif mode == 'dub':
                final_path = dub_video(raw_path)
            else:
                final_path = raw_path

            @after_this_request
            def cleanup(response):
                try:
                    # استخدام set لحذف الملفات دون تكرار
                    for f in {raw_path, final_path}:
                        if f and os.path.exists(f): os.remove(f)
                except Exception as e:
                    logger.error(f"Cleanup Error: {e}")
                return response

            return send_file(final_path, as_attachment=True)

    except Exception as e:
        logger.error(f"Kernel Error: {str(e)}")
        return jsonify({"status": "failed", "error": str(e)}), 500

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
    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
