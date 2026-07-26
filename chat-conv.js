async function showConvList() {
    const list = document.getElementById('convList');
    list.innerHTML = '<div style="text-align:center;padding:20px;color:#94a3b8;">加载中...</div>';
    showModal('convModal');
    try {
        const convs = await getAllConvs();
        convs.sort((a, b) => (b.time || 0) - (a.time || 0));

        if (convs.length === 0) {
            list.innerHTML = '<div style="text-align:center;padding:20px;color:#94a3b8;">暂无保存的对话</div>';
        } else {
            list.innerHTML = convs.map(c => {
                const msgs = (c.messages || []).filter(m => m.role !== 'system');
                const first = msgs[0]?.content?.slice(0, 40) || '(空)';
                const t = c.time ? new Date(c.time).toLocaleString() : '';
                const active = c.id === currentConvId ? 'background:#eef2ff;' : '';
                return `<div class="conv-item" style="${active}" onclick="loadConv('${c.id}')">
                    <span class="conv-name">${escapeHtml(first)}${msgs.length > 1 ? '...' : ''}</span>
                    <span class="conv-meta">${msgs.length}条 ${t}</span>
                    <button class="conv-del" onclick="event.stopPropagation();deleteConv('${c.id}')" title="删除">✕</button>
                </div>`;
            }).join('');
        }
    } catch (e) { toast('加载历史失败'); }
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
        hideModal('convModal');

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
        toast('已加载对话');
    } catch (e) { toast('加载对话失败'); }
}

async function deleteConv(id) {
    if (!confirm('删除此对话？')) return;
    try {
        await deleteConvById(id);
        if (id === currentConvId) currentConvId = null;
        showConvList();
    } catch (e) { toast('删除失败'); }
}

function newChat() {
    if (messages.length > 1) autoSave();
    messages = [{ role: 'system', content: config.system }];
    currentConvId = null;
    document.getElementById('messages').innerHTML = '<div class="empty-state">💬 新对话</div>';
    updateStats();
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
