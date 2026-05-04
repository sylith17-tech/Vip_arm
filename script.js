// ==========================================================
// [KERNEL-0x0] - MASTER CONTROL MATRIX v4.0
// IDENTITY: VIP_ARM SYSTEM ENGINE
// ==========================================================

const Kernel = {
    // 1. بروتوكول التشغيل الرئيسي
    init() {
        console.log("%c VIP_ARM Secure Engine: Matrix Initiated ", "background: #bc13fe; color: #fff; font-weight: bold;");
        this.UI.typewriter();
        this.Studio.init();
        this.Security.initProtection();
    },

    // 2. محرك الاستوديو ومعالجة الصور
    Studio: {
        init() {
            const imageInput = document.getElementById('imageInput') || document.getElementById('imageLoader');
            const mainCanvas = document.getElementById('mainCanvas');
            if (!imageInput || !mainCanvas) return;

            const ctx = mainCanvas.getContext('2d');
            imageInput.addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;

                Kernel.UI.log(`INJECTING_DATA: ${file.name} [${(file.size / 1024).toFixed(2)} KB]`);

                const reader = new FileReader();
                reader.onload = (event) => {
                    const img = new Image();
                    img.onload = () => {
                        mainCanvas.width = img.width;
                        mainCanvas.height = img.height;
                        ctx.drawImage(img, 0, 0);

                        // تحديث بيانات الدقة
                        const resDisplay = document.querySelector('.res-val');
                        if (resDisplay) resDisplay.innerText = `${img.width}x${img.height}`;

                        document.getElementById('dropPrompt')?.style.setProperty('display', 'none');
                        mainCanvas.style.display = 'block';

                        Kernel.UI.updateStatus('IMAGE_LOADED // SUCCESS');
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);

                // المزامنة مع السيرفر
                this.sync(file);
            });
        },

        async sync(file) {
            const formData = new FormData();
            formData.append('image', file);
            try {
                Kernel.UI.updateStatus('UPLOADING_TO_KERNEL...');
                const response = await fetch('/upload', { method: 'POST', body: formData });
                if (response.ok) {
                    Kernel.UI.updateStatus('SYNC_COMPLETED // NODE: Kernel-0x0');
                    Kernel.UI.log("SERVER_SYNC: SUCCESSFUL");
                } else {
                    Kernel.UI.updateStatus('SYNC_ERROR // LOCAL_MODE');
                }
            } catch (err) {
                Kernel.UI.updateStatus('OFFLINE_MODE // RENDER_ONLY');
            }
        }
    },

    // 3. محرك الاستخراج الذكي (Media Intelligence)
    Media: {
        async startExtraction() {
            const urlInput = document.getElementById('targetUrl');
            const btn = document.getElementById('extractBtn') || document.getElementById('dlBtn');
            const results = document.getElementById('results') || document.getElementById('resultArea');

            if (!urlInput || !urlInput.value) {
                Kernel.UI.log("ERROR: TARGET_URL_NULL", "danger");
                return alert("Target URL Missing!");
            }

            // تحديث واجهة المستخدم لبدء الاستخراج
            btn.innerText = "BYPASSING...";
            btn.disabled = true;
            Kernel.UI.log(`INITIATING_RECON: ${urlInput.value}`);

            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: urlInput.value })
                });

                const contentType = response.headers.get("content-type");

                if (response.ok && contentType?.includes("application/json")) {
                    const data = await response.json();
                    if (data.status === "success") {
                        this.renderResults(data, results);
                        Kernel.UI.log("EXTRACTION_COMPLETE: ASSETS_READY");
                    } else {
                        throw new Error(data.error || "Unknown Server Error");
                    }
                } else if (response.ok) {
                    // معالجة التحميل المباشر للملفات (Blob)
                    const blob = await response.blob();
                    this.forceDownload(blob);
                } else {
                    throw new Error(`HTTP Error: ${response.status}`);
                }
            } catch (err) {
                Kernel.UI.log(`SECURITY_BREACH: ${err.message}`, "danger");
                alert("Security Breach: " + err.message);
            } finally {
                btn.innerText = "EXTRACT DATA";
                btn.disabled = false;
            }
        },

        renderResults(data, container) {
            if (!container) return;
            container.style.display = 'block';

            // تحديث العناصر إن وجدت (دعم downloader.html)
            const titleEl = document.getElementById('resTitle') || document.getElementById('videoTitle');
            const thumbEl = document.getElementById('resThumb');
            const mainDl = document.getElementById('mainDownloadBtn') || document.getElementById('dlLink');

            if (titleEl) titleEl.innerText = data.title;
            if (thumbEl) thumbEl.src = data.thumbnail;

            // تحديث قائمة الصيغ (إن وجدت)
            const list = document.getElementById('formatList');
            if (list && data.formats) {
                list.innerHTML = '';
                data.formats.forEach(f => {
                    const tr = `<tr>
                        <td><span class="badge">${f.ext.toUpperCase()}</span></td>
                        <td>${f.resolution || 'N/A'}</td>
                        <td>${f.filesize || '--'}</td>
                        <td><a href="${f.url}" target="_blank" class="dl-icon-btn">GET</a></td>
                    </tr>`;
                    list.innerHTML += tr;
                });
            }

            // تعيين رابط التحميل الرئيسي
            if (mainDl && data.formats && data.formats[0]) {
                mainDl.href = data.formats[0].url;
            }
        },

        forceDownload(blob) {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `VIP_ARM_CONTENT_${Date.now()}.mp4`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            Kernel.UI.log("DIRECT_STREAM_CAPTURED");
        }
    },

    // 4. الماسح الأمني المحسن
    Security: {
        async runScan() {
            const scanInput = document.getElementById('scanTarget');
            const resDiv = document.getElementById('scanResults');
            if (!scanInput || !scanInput.value) return;

            Kernel.UI.log(`PROBING_HOST: ${scanInput.value}`);
            resDiv.innerHTML = "<span class='blink'>PROBING TARGET...</span>";

            try {
                const response = await fetch('/api/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: scanInput.value })
                });
                const report = await response.json();
                resDiv.innerHTML = `<pre class="scan-report">${JSON.stringify(report, null, 2)}</pre>`;
                Kernel.UI.log("SCAN_REPORT_GENERATED");
            } catch (e) {
                resDiv.innerHTML = "<span style='color:red'>Scan Failed: Connection Refused</span>";
                Kernel.UI.log("SCAN_ABORTED: HOST_UNREACHABLE", "danger");
            }
        },

        initProtection() {
            document.addEventListener('contextmenu', e => e.preventDefault());
            window.addEventListener('keydown', e => {
                if(e.ctrlKey && (e.key === 'u' || e.key === 's')) e.preventDefault();
            });
        }
    },

    // 5. واجهة المستخدم والتأثيرات (Aesthetic Engine)
    UI: {
        log(msg, type = "info") {
            const consoleBox = document.getElementById('consoleFeed');
            if (consoleBox) {
                consoleBox.style.display = 'block';
                consoleBox.innerHTML = `> <span style="color: ${type === 'danger' ? '#ff3e3e' : '#00ff41'}">${msg}</span>`;
            }
            console.log(`[KERNEL-LOG]: ${msg}`);
        },

        updateStatus(msg) {
            const statusMsg = document.getElementById('statusMsg');
            if (statusMsg) statusMsg.innerText = msg;
        },

        typewriter() {
            document.querySelectorAll('.typewriter').forEach(title => {
                let text = title.innerText;
                title.innerText = '';
                let i = 0;
                const type = () => {
                    if (i < text.length) {
                        title.innerText += text.charAt(i++);
                        setTimeout(type, 50);
                    }
                };
                type();
            });
        }
    }
};

// ربط الوظائف بـ Window لضمان عمل أزرار HTML (OnClick)
window.processExtraction = () => Kernel.Media.startExtraction();
window.startDownload = () => Kernel.Media.startExtraction(); // دعم التسمية القديمة
window.runScan = () => Kernel.Security.runScan();
window.sendToCloud = () => {
    Kernel.UI.log("UPLINKING TO TELEGRAM BOT...");
    alert("Mastermind Sync: Uplinking to Telegram via VIP_ARM OS.");
};

// تشغيل النظام عند التحميل
document.addEventListener('DOMContentLoaded', () => Kernel.init());
