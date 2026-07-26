function showModal(id) { document.getElementById(id).classList.add('show'); }
function hideModal(id) { document.getElementById(id).classList.remove('show'); }

function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 2000);
}

function escapeHtml(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
}

function marked(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

function updateStats() {
    const nonSys = messages.filter(m => m.role !== 'system');
    const chars = nonSys.reduce((s, m) => s + (m.content || '').length + (m.reasoning_content || '').length, 0);
    document.getElementById('statMsgs').textContent = `消息: ${nonSys.length}`;
    document.getElementById('statChars').textContent = `字符: ${chars}`;
    document.getElementById('statTokens').textContent = `预估 Token: ${Math.ceil(chars / 3.5)}`;
}
