// ==========================================
// [KERNEL-0x0] - CENTRAL CONTROL SCRIPT
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log("VIP_ARM Secure Engine: Initiated");
    
    // 1. نظام رفع ومعالجة الصور (Image Injection)
    const imageInput = document.getElementById('imageInput');
    const mainCanvas = document.getElementById('mainCanvas');
    
    if (imageInput && mainCanvas) {
        const ctx = mainCanvas.getContext('2d');
        
        imageInput.addEventListener('change', (e) => {
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    // ضبط أبعاد الكانفاس لتناسب الصورة
                    mainCanvas.width = img.width;
                    mainCanvas.height = img.height;
                    ctx.drawImage(img, 0, 0);
                    
                    // تحديث الوضوح في الفوتر
                    const resolutionDisplay = document.querySelector('.res-val');
                    if(resolutionDisplay) resolutionDisplay.innerText = `${img.width}x${img.height}`;
                    
                    console.log("Image Injected Successfully into Kernel-0x0");
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(e.target.files[0]);
        });
    }

    // 2. محرك التحميل (Media Downloader)
    window.startDownload = async () => {
        const url = document.getElementById('targetUrl').value;
        const btn = document.getElementById('dlBtn');
        if(!url) return alert("Target URL Missing!");

        btn.innerText = "EXTRACTING...";
        try {
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            });
            const data = await response.json();
            if(data.status === "success") {
                // عرض البيانات (تأكد من وجود هذه العناصر في downloader.html)
                document.getElementById('videoTitle').innerText = data.intel.title;
                document.getElementById('dlLink').href = data.intel.dl_link;
                document.getElementById('resultArea').style.display = 'block';
            } else {
                alert("Extraction Failed: " + data.error);
            }
        } catch (err) {
            console.error("Signal Lost:", err);
        } finally {
            btn.innerText = "START RECON";
        }
    };

    // 3. الماسح الأمني (Security Scanner)
    window.runScan = async () => {
        const target = document.getElementById('scanTarget').value;
        if(!target) return;
        
        const resDiv = document.getElementById('scanResults');
        resDiv.innerHTML = "PROBING TARGET...";
        
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: target})
        });
        const report = await response.json();
        resDiv.innerHTML = `<pre>${JSON.stringify(report, null, 2)}</pre>`;
    };

    // 4. تأثيرات الكتابة (Typewriter)
    const titles = document.querySelectorAll('.typewriter');
    titles.forEach(title => {
        let text = title.innerText;
        title.innerText = '';
        let i = 0;
        function type() {
            if (i < text.length) {
                title.innerText += text.charAt(i);
                i++;
                setTimeout(type, 50);
            }
        }
        type();
    });
});

// بروتوكول الحماية
document.addEventListener('contextmenu', e => e.preventDefault());
