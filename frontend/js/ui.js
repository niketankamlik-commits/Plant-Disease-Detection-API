/**
 * ui.js — Common UI interactions (blobs, loader)
 * Used by: all pages
 */
document.addEventListener('DOMContentLoaded', () => {

    // Blob mouse parallax effect
    const blobs = document.querySelectorAll('.blob');
    if (blobs.length > 0) {
        document.addEventListener('mousemove', (e) => {
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            blobs.forEach((blob, index) => {
                const speed = (index + 1) * 20;
                blob.style.transform = `translate(${(x - 0.5) * speed}px, ${(y - 0.5) * speed}px)`;
            });
        });
    }

    // Loader fade-out (index page only)
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => {
            loader.style.opacity = '0';
            loader.style.visibility = 'hidden';
        }, 2000);
    }

    // Password show/hide toggle
    const toggleBtn = document.getElementById('togglePassword');
    if (toggleBtn) {
        toggleBtn.onclick = () => {
            const input = document.getElementById('password');
            const isPass = input.type === 'password';
            input.type = isPass ? 'text' : 'password';
            toggleBtn.querySelector('.eye-open').style.display = isPass ? 'none' : 'block';
            toggleBtn.querySelector('.eye-closed').style.display = isPass ? 'block' : 'none';
        };
    }
});
