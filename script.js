// ==========================================
// [KERNEL-0x0] - ADVANCED CENTRAL CONTROL SCRIPT
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log("VIP_ARM Secure Engine: Initiated");

    // 1. نظام معالجة الصور (Image Injection & Studio Support)
    // التعديل: دعم كلاً من imageInput (للموقع العام) و imageLoader (للاستوديو)
    const imageInput = document.getElementById('imageInput') || document.getElementById('imageLoader');
    const mainCanvas = document.getElementById('mainCanvas');

    if (imageInput && mainCanvas) {
        const ctx = mainCanvas.getContext('2d');
        imageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    mainCanvas.width = img.width;
                    mainCanvas.height = img.height;
                    ctx.drawImage(img, 0, 0);
                    
                    // تحديث بيانات الدقة إن وجدت
                    const resDisplay = document.querySelector('.res-val');
                    if(resDisplay) resDisplay.innerText = `${img.width}x${img.height}`;
                    
                    // إخفاء موجه السحب في الاستوديو إن وجد
                    const dropPrompt = document.getElementById('dropPrompt');
                    if(dropPrompt) dropPrompt.style.display = 'none';
                    mainCanvas.style.display = 'block';
                    
                    // تحديث الحالة لبروتوكول VIP_ARM
                    updateKernelStatus('IMAGE_LOADED // SUCCESS');
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);

            // بروتوكول الرفع التلقائي للسيرفر (Back-end Sync)
            uploadToKernel(file);
        });
    }

    // وظيفة الرفع الخاصة بـ Kernel-0x0
    async function uploadToKernel(file) {
        const formData = new FormData();
        formData.append('image', file); 

        try {
            updateKernelStatus('UPLOADING_TO_KERNEL...');
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                updateKernelStatus('SYNC_COMPLETED // NODE: Kernel-0x0');
            } else {
                updateKernelStatus('SYNC_ERROR // LOCAL_MODE');
            }
        } catch (err) {
            updateKernelStatus('OFFLINE_MODE // RENDER_ONLY');
        }
    }

    function updateKernelStatus(msg) {
        const statusMsg = document.getElementById('statusMsg');
        if(statusMsg) statusMsg.innerText = msg;
    }

    // 2. محرك التحميل المطور (The Fix for undefined)
    window.startDownload = async () => {
        const urlInput = document.getElementById('targetUrl');
        const btn = document.getElementById('dlBtn');
        const resultArea = document.getElementById('resultArea');

        if(!urlInput || !urlInput.value) return alert("Target URL Missing!");

        btn.innerText = "BYPASSING...";
        btn.disabled = true;

        try {
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: urlInput.value})
            });

            const contentType = response.headers.get("content-type");

            if (response.ok && contentType && contentType.includes("application/json")) {
                const data = await response.json();
                if(data.status === "success") {
                    // التعديل: التعامل مع هيكل البيانات المرسل من app.py (data.formats أو data.title)
                    const videoTitle = document.getElementById('videoTitle');
                    if(videoTitle) videoTitle.innerText = data.title || "Media Found";
                    
                    const dlLink = document.getElementById('dlLink');
                    if(dlLink && data.formats && data.formats[0]) dlLink.href = data.formats[0].url;
                    
                    if(resultArea) resultArea.style.display = 'block';
                } else {
                    throw new Error(data.error || "Unknown Server Error");
                }
            }
            else if (response.ok) {
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
            alert("Security Breach: " + err.message);
        } finally {
            if(btn) {
                btn.innerText = "START RECON";
                btn.disabled = false;
            }
        }
    };

    // 3. الماسح الأمني المحسن
    window.runScan = async () => {
        const scanInput = document.getElementById('scanTarget');
        const resDiv = document.getElementById('scanResults');
        if(!scanInput || !scanInput.value) return;

        resDiv.innerHTML = "<span class='blink'>PROBING TARGET...</span>";

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: scanInput.value})
            });
            const report = await response.json();
            resDiv.innerHTML = `<pre class="scan-report">${JSON.stringify(report, null, 2)}</pre>`;
        } catch (e) {
            if(resDiv) resDiv.innerHTML = "Scan Failed: Connection Refused";
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
