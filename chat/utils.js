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
    if (!text) return '';
    const escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    const codeBlocks = [];
    let html = escaped.replace(/```(\w*)\n?([\s\S]*?)```/g, (match, lang, code) => {
        const idx = codeBlocks.length;
        const langAttr = lang ? ` class="lang-${escapeHtml(lang)}"` : '';
        const codeId = 'cb' + Date.now() + idx;
        codeBlocks.push(`<pre><code${langAttr} id="${codeId}">${code.trim()}</code><button class="copy-code-btn" onclick="copyCode('${codeId}')">📋</button></pre>`);
        return `%%CODEBLOCK${idx}%%`;
    });

    const lines = html.split('\n');
    const out = [];
    let inUl = false, inOl = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];

        const cbMatch = line.match(/^%%CODEBLOCK(\d+)%%$/);
        if (cbMatch) {
            if (inUl) { out.push('</ul>'); inUl = false; }
            if (inOl) { out.push('</ol>'); inOl = false; }
            out.push(codeBlocks[parseInt(cbMatch[1])]);
            continue;
        }

        if (/^#{1,3}\s/.test(line)) {
            if (inUl) { out.push('</ul>'); inUl = false; }
            if (inOl) { out.push('</ol>'); inOl = false; }
            const level = line.match(/^(#+)\s/)[1].length;
            const tag = 'h' + level;
            const content = line.replace(/^#+\s/, '');
            out.push(`<${tag}>${inlineMarkdown(content)}</${tag}>`);
            continue;
        }

        if (/^>\s/.test(line)) {
            if (inUl) { out.push('</ul>'); inUl = false; }
            if (inOl) { out.push('</ol>'); inOl = false; }
            out.push(`<blockquote>${inlineMarkdown(line.replace(/^>\s/, ''))}</blockquote>`);
            continue;
        }

        if (/^- \s/.test(line)) {
            if (inOl) { out.push('</ol>'); inOl = false; }
            if (!inUl) { out.push('<ul>'); inUl = true; }
            out.push(`<li>${inlineMarkdown(line.replace(/^- \s/, ''))}</li>`);
            continue;
        }

        if (/^\d+\.\s/.test(line)) {
            if (inUl) { out.push('</ul>'); inUl = false; }
            if (!inOl) { out.push('<ol>'); inOl = true; }
            out.push(`<li>${inlineMarkdown(line.replace(/^\d+\.\s/, ''))}</li>`);
            continue;
        }

        if (line.trim() === '') {
            if (inUl) { out.push('</ul>'); inUl = false; }
            if (inOl) { out.push('</ol>'); inOl = false; }
            continue;
        }

        if (inUl) { out.push('</ul>'); inUl = false; }
        if (inOl) { out.push('</ol>'); inOl = false; }
        out.push(`<p>${inlineMarkdown(line)}</p>`);
    }

    if (inUl) out.push('</ul>');
    if (inOl) out.push('</ol>');

    return out.join('\n');
}

function inlineMarkdown(text) {
    return text
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>');
}

function copyCode(id) {
    const el = document.getElementById(id);
    if (!el) return;
    const text = el.textContent;
    navigator.clipboard.writeText(text).then(
        () => toast('已复制'),
        () => toast('复制失败')
    );
}

function updateStats() {
    const nonSys = messages.filter(m => m.role !== 'system');
    const chars = nonSys.reduce((s, m) => s + (m.content || '').length + (m.reasoning_content || '').length, 0);
    document.getElementById('statMsgs').textContent = `消息: ${nonSys.length}`;
    document.getElementById('statChars').textContent = `字符: ${chars}`;
    document.getElementById('statTokens').textContent = `预估 Token: ${Math.ceil(chars / 3.5)}`;
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    document.getElementById('themeIcon').textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('aichat_theme', isDark ? 'dark' : 'light');
}

function loadTheme() {
    const saved = localStorage.getItem('aichat_theme');
    if (saved === 'dark') {
        document.documentElement.classList.add('dark');
        document.getElementById('themeIcon').textContent = '☀️';
    }
}
