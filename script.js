// ==========================================
// [KERNEL-0x0] - ADVANCED CENTRAL CONTROL SCRIPT 
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log("VIP_ARM Secure Engine: Initiated");

    // 1. نظام معالجة الصور (Image Injection)
    const imageInput = document.getElementById('imageInput');
    const mainCanvas = document.getElementById('mainCanvas');

    if (imageInput && mainCanvas) {
        const ctx = mainCanvas.getContext('2d');
        imageInput.addEventListener('change', (e) => {
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    mainCanvas.width = img.width;
                    mainCanvas.height = img.height;
                    ctx.drawImage(img, 0, 0);
                    const resDisplay = document.querySelector('.res-val');
                    if(resDisplay) resDisplay.innerText = `${img.width}x${img.height}`;
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(e.target.files[0]);
        });
    }

    // 2. محرك التحميل المطور (The Fix for undefined)
    window.startDownload = async () => {
        const urlInput = document.getElementById('targetUrl');
        const btn = document.getElementById('dlBtn');
        const resultArea = document.getElementById('resultArea');
        
        if(!urlInput.value) return alert("Target URL Missing!");

        btn.innerText = "BYPASSING...";
        btn.disabled = true;

        try {
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: urlInput.value})
            });

            // التحقق من نوع الاستجابة (هل هي JSON أم ملف؟)
            const contentType = response.headers.get("content-type");

            if (response.ok && contentType && contentType.includes("application/json")) {
                const data = await response.json();
                if(data.status === "success") {
                    document.getElementById('videoTitle').innerText = data.intel.title;
                    document.getElementById('dlLink').href = data.intel.dl_link;
                    if(resultArea) resultArea.style.display = 'block';
                } else {
                    throw new Error(data.error || "Unknown Server Error");
                }
            } 
            else if (response.ok) {
                // إذا أرسل السيرفر ملفاً مباشرة (Blob)
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = `VIP_ARM_CONTENT_${Date.now()}.mp4`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                alert("Download Started Successfully!");
            }
            else {
                throw new Error(`HTTP Error: ${response.status}`);
            }

        } catch (err) {
            console.error("Signal Lost:", err);
            // حل مشكلة الصورة "تعذر الاتصال بالمحرك"
            alert("Security Breach: " + err.message);
        } finally {
            btn.innerText = "START RECON";
            btn.disabled = false;
        }
    };

    // 3. الماسح الأمني المحسن
    window.runScan = async () => {
        const target = document.getElementById('scanTarget').value;
        const resDiv = document.getElementById('scanResults');
        if(!target) return;

        resDiv.innerHTML = "<span class='blink'>PROBING TARGET...</span>";

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: target})
            });
            const report = await response.json();
            resDiv.innerHTML = `<pre class="scan-report">${JSON.stringify(report, null, 2)}</pre>`;
        } catch (e) {
            resDiv.innerHTML = "Scan Failed: Connection Refused";
        }
    };

    // 4. تأثيرات Typewriter (Kernel Aesthetic)
    const titles = document.querySelectorAll('.typewriter');
    titles.forEach(title => {
        let text = title.innerText;
        title.innerText = '';
        let i = 0;
        (function type() {
            if (i < text.length) {
                title.innerText += text.charAt(i++);
                setTimeout(type, 50);
            }
        }());
    });
});

// بروتوكول الحماية
document.addEventListener('contextmenu', e => e.preventDefault());
