// Kernel-0x0 Core System Script
document.addEventListener('DOMContentLoaded', () => {
    console.log("Kernel-0x0 System Online...");
    
    // Auto-Type Effect for Titles
    const titles = document.querySelectorAll('.typewriter');
    titles.forEach(title => {
        let text = title.innerText;
        title.innerText = '';
        let i = 0;
        function type() {
            if (i < text.length) {
                title.innerText += text.charAt(i);
                i++;
                setTimeout(type, 100);
            }
        }
        type();
    });

    // Device Info Detection (Internal Use)
    const statusFooter = document.querySelector('.terminal-footer');
    if(statusFooter) {
        const platform = navigator.platform;
        statusFooter.innerText += ` // OS: ${platform} // ENV: NETHUNTER`;
    }
});

// Secure Lockdown (Prevent Inspection)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && (e.key === 'u' || e.key === 's' || e.key === 'i')) {
        e.preventDefault();
        alert("SECURITY ALERT: UNUATHORIZED ACCESS BLOCKED");
    }
});
