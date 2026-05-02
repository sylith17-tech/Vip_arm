from flask import Flask, render_template, send_from_directory, abort
import os

# إعداد التطبيق - Flask سيبحث عن ملفات HTML في المجلد الرئيسي مباشرة
app = Flask(__name__, template_folder='.')

# المسار الرئيسي للموقع
@app.route('/')
def index():
    try:
        # تشغيل لوحة التحكم الرئيسية
        return render_template('index.html')
    except Exception:
        return "Error: index.html not found in root directory."

# محرك ديناميكي لربط جميع الصفحات (contact.html, scanner.html, إلخ)
@app.route('/<page_name>.html')
def render_page(page_name):
    file_path = f"{page_name}.html"
    if os.path.exists(file_path):
        return render_template(file_path)
    else:
        abort(404)

# توجيه الملفات المساعدة (CSS, JS, Images) لضمان عمل التصميم
@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('.', filename)

# معالج أخطاء 404 بتصميم بسيط (يمكنك تخصيصه لاحقاً)
@app.errorhandler(404)
def page_not_found(e):
    return "<h1 style='color:gold; background:black; text-align:center;'>404 | KERNEL-0X0 ERROR: ACCESS DENIED</h1>", 404

if __name__ == '__main__':
    # البورت الافتراضي 5000 وهو ما يبحث عنه Render عادةً
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
