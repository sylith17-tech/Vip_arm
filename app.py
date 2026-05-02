import os
import yt_dlp
import logging
import uuid
from flask import Flask, render_template, request, jsonify, send_file, after_this_request
from flask_cors import CORS
from PIL import Image
from PIL.ExifTags import TAGS
# تصحيح الاستدعاء ليتوافق مع MoviePy 2.2.1
from moviepy import VideoFileClip, vfx 
from gtts import gTTS

# [CENTRAL_INTELLIGENCE_CORE] - NODE: Kernel-0x0
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [NODE_ID: Kernel-0x0] - %(message)s'
)
logger = logging.getLogger(__name__)

# إعداد التطبيق ليعمل في المجلد الرئيسي مباشرة (بناءً على قائمة ls الخاصة بك)
app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def get_ydl_opts(custom_out=None):
    return {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': custom_out or os.path.join(DOWNLOAD_FOLDER, 'VIP_ARM_%(id)s.%(ext)s'),
        'nocheckcertificate': True,
        'quiet': True
    }

# --- ميزة 1: المخرج الآلي (Auto-Shorts) ---
def create_shorts(input_path):
    output_path = input_path.replace(".mp4", "_SHORTS.mp4")
    with VideoFileClip(input_path) as video:
        duration = min(video.duration, 60)
        clip = video.subclip(0, duration)
        w, h = clip.size
        target_ratio = 9/16
        target_w = h * target_ratio
        final_clip = clip.crop(x_center=w/2, width=target_w)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

# --- ميزة 2: الدبلجة العصبية المبسطة ---
def dub_video(input_path, lang='ar'):
    output_path = input_path.replace(".mp4", "_DUBBED.mp4")
    temp_audio = f"temp_{uuid.uuid4()}.mp3"
    with VideoFileClip(input_path) as video:
        tts = gTTS(text="تمت المعالجة بواسطة محرك VIP_ARM", lang=lang)
        tts.save(temp_audio)
        video.set_audio(VideoFileClip(temp_audio).audio).write_videofile(output_path)
    if os.path.exists(temp_audio): os.remove(temp_audio)
    return output_path

# --- ربط الصفحات (Routes) لضمان عدم ظهور 404 ---

@app.route('/')
def index(): 
    return render_template('index.html')

# ربط ديناميكي لكل ملفات HTML الموجودة في المجلد لتعمل تلقائياً
@app.route('/<page>')
def serve_pages(page):
    if page.endswith('.html'):
        return render_template(page)
    # إذا طلب المستخدم /downloader مثلاً بدون .html
    if os.path.exists(f"{page}.html"):
        return render_template(f"{page}.html")
    return render_template('index.html'), 404

# --- API Endpoints ---

@app.route('/api/process', methods=['POST'])
def handle_advanced_process():
    data = request.json
    url = data.get('url')
    mode = data.get('mode') 

    try:
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
            # تنظيف الملفات بعد الإرسال لتوفير مساحة Kernel-0x0
            try:
                for f in [raw_path, final_path]:
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
