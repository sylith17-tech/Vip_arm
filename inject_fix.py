import os

js_fix = """
<script>
function handleFileUpload(file) {
    if (!file) return;
    console.log("جاري رفع الملف: " + file.name);
    let formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert("تم الرفع بنجاح!");
        location.reload();
    })
    .catch(error => {
        console.error("خطأ في الرفع:", error);
        alert("فشل الرفع، تفقد سجلات السيرفر");
    });
}
</script>
"""

target_files = ['exif.html', 'forensic.html']

for file_path in target_files:
    if os.path.exists(file_path):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(js_fix)
        print(f"[+] تم إضافة منطق الرفع إلى: {file_path}")
