config = loadConfig();
params = loadParams();
messages = [{ role: 'system', content: config.system }];

document.querySelectorAll('.modal').forEach(m => {
    m.addEventListener('click', function(e) { if (e.target === this) this.classList.remove('show'); });
});

document.getElementById('input').addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

window.addEventListener('beforeunload', () => autoSave());
