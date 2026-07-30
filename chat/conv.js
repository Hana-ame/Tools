async function renderConvList() {
    const list = document.getElementById('convList');
    try {
        const convs = await getAllConvs();
        convs.sort((a, b) => (b.time || 0) - (a.time || 0));

        if (convs.length === 0) {
            list.innerHTML = '<div class="conv-list-empty">暂无对话</div>';
            return;
        }

        const filter = (document.getElementById('convSearch').value || '').toLowerCase();
        let html = '';
        for (const c of convs) {
            const msgs = (c.messages || []).filter(m => m.role !== 'system');
            const first = msgs[0]?.content?.slice(0, 40) || '(空)';
            const t = c.time ? new Date(c.time).toLocaleString() : '';
            const active = c.id === currentConvId ? 'active' : '';

            if (filter && !first.toLowerCase().includes(filter)) continue;

            html += `<div class="conv-item ${active}" data-id="${c.id}" onclick="loadConv('${c.id}')">
                <span class="conv-name" title="${escapeHtml(first)}">${escapeHtml(first)}</span>
                <span class="conv-meta">${msgs.length}条</span>
                <span class="conv-actions">
                    <button onclick="event.stopPropagation();showRename('${c.id}')" title="重命名">✏️</button>
                    <button onclick="event.stopPropagation();deleteConv('${c.id}')" title="删除">🗑️</button>
                </span>
            </div>`;
        }
        if (!html) html = '<div class="conv-list-empty">无匹配对话</div>';
        list.innerHTML = html;
    } catch (e) {
        list.innerHTML = '<div class="conv-list-empty">加载失败</div>';
    }
}

function filterConvs(val) {
    renderConvList();
}

async function loadConv(id) {
    try {
        const c = await getConvById(id);
        if (!c) return;
        messages = c.messages.map(m => ({ ...m, _id: m._id || nextId() }));
        config = c.config || config;
        if (c.params && 'json' in c.params) {
            params = c.params;
        } else if (c.params) {
            const old = c.params;
            const obj = {};
            if (old.max_tokens) obj.max_tokens = old.max_tokens;
            if (old.temperature) obj.temperature = old.temperature;
            if (old.top_p) obj.top_p = old.top_p;
            if (old.thinking === 'true') obj.enable_thinking = true;
            else if (old.thinking === 'false') obj.enable_thinking = false;
            if (old.extra) { try { Object.assign(obj, JSON.parse(old.extra)); } catch {} }
            params = { mode: 'table', json: JSON.stringify(obj, null, 2) };
        }
        currentConvId = id;

        const container = document.getElementById('messages');
        container.innerHTML = '';
        for (let i = 0; i < messages.length; i++) {
            const m = messages[i];
            if (m.role === 'system') continue;
            addMsg(m.role, m.content, m.reasoning_content, m._id);
        }
        if (!container.querySelector('.msg')) {
            container.innerHTML = '<div class="empty-state">💬 已加载对话</div>';
        }
        updateStats();
        renderConvList();

        if (window.innerWidth <= 700) {
            document.getElementById('sidebar').classList.remove('open');
        }
    } catch (e) { toast('加载对话失败'); }
}

async function deleteConv(id) {
    if (!confirm('删除此对话？')) return;
    try {
        await deleteConvById(id);
        if (id === currentConvId) {
            currentConvId = null;
            messages = [{ role: 'system', content: config.system }];
            document.getElementById('messages').innerHTML = '<div class="empty-state">💬 对话已删除</div>';
            updateStats();
        }
        renderConvList();
    } catch (e) { toast('删除失败'); }
}

let renamingId = null;
function showRename(id) {
    renamingId = id;
    document.getElementById('renameInput').value = '';
    showModal('renameModal');
    setTimeout(() => document.getElementById('renameInput').focus(), 100);
}

async function doRename() {
    const name = document.getElementById('renameInput').value.trim();
    if (!name || !renamingId) { hideModal('renameModal'); return; }
    try {
        const c = await getConvById(renamingId);
        if (c) {
            c.name = name;
            await putConv(c);
            renderConvList();
        }
    } catch (e) { toast('重命名失败'); }
    hideModal('renameModal');
    renamingId = null;
}

function newChat() {
    if (messages.length > 1) autoSave();
    messages = [{ role: 'system', content: config.system }];
    currentConvId = null;
    document.getElementById('messages').innerHTML = '<div class="empty-state">💬 新对话</div>';
    updateStats();
    renderConvList();
    document.getElementById('hdrTitle').textContent = 'AI Chat';
}

function copyMessages() {
    const msgs = messages.filter(m => m.role !== 'system');
    if (msgs.length === 0) { toast('没有可复制的消息'); return; }
    const text = JSON.stringify(msgs, null, 2);
    navigator.clipboard.writeText(text).then(
        () => toast('messages[] 已复制'),
        () => toast('复制失败')
    );
}
