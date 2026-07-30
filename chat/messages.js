function addMsg(role, text, thinking, msgId) {
    const container = document.getElementById('messages');
    const empty = container.querySelector('.empty-state');
    if (empty) empty.remove();

    const mid = msgId || nextId();
    const div = document.createElement('div');
    div.className = `msg ${role}`;
    div.dataset.mid = mid;

    const actions = document.createElement('div');
    actions.className = 'msg-actions';
    actions.innerHTML = '<button onclick="editMsg(this)">✏️</button><button onclick="deleteMsg(this)">🗑️</button><button onclick="copyMsg(this)">📋</button><button onclick="forkFrom(this)">🔀</button>';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    if (role === 'ai' && thinking) {
        const t = buildThinking(thinking);
        bubble.appendChild(t);
    }
    if (role === 'ai') {
        bubble.innerHTML += marked(text || '');
    } else {
        bubble.textContent = text;
    }
    div.appendChild(bubble);
    div.appendChild(actions);

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    updateStats();
    return div;
}

function buildThinking(text) {
    const div = document.createElement('div');
    div.className = 'thinking';
    div.onclick = function(e) {
        if (e.target.closest('.copy-code-btn')) return;
        this.classList.toggle('collapsed');
        const t = this.querySelector('.thinking-toggle');
        if (t) t.textContent = this.classList.contains('collapsed') ? '▶ 展开' : '▼ 收起';
    };
    const toggle = document.createElement('span');
    toggle.className = 'thinking-toggle';
    toggle.textContent = '▼ 收起';
    const content = document.createElement('div');
    content.className = 'thinking-content';
    content.textContent = text;
    div.appendChild(toggle);
    div.appendChild(content);
    return div;
}

function updateBubble(el, text, thinking) {
    const bubble = el.querySelector('.bubble');
    bubble.innerHTML = '';
    if (thinking) {
        const t = buildThinking(thinking);
        bubble.appendChild(t);
    }
    bubble.innerHTML += marked(text || '');
}

function copyMsg(btn) {
    const msgDiv = btn.closest('.msg');
    const mid = parseInt(msgDiv.dataset.mid);
    const idx = findMsg(mid);
    if (idx < 0) return;
    const text = messages[idx].content;
    navigator.clipboard.writeText(text).then(
        () => toast('已复制'),
        () => toast('复制失败')
    );
}

function editMsg(btn) {
    const msgDiv = btn.closest('.msg');
    const mid = parseInt(msgDiv.dataset.mid);
    const idx = findMsg(mid);
    if (idx < 0) return;
    const bubble = msgDiv.querySelector('.bubble');
    if (msgDiv.classList.contains('editing')) return;

    const originalText = messages[idx].content;
    msgDiv.classList.add('editing');
    bubble.innerHTML = '';

    const ta = document.createElement('textarea');
    ta.value = originalText;
    bubble.appendChild(ta);
    ta.focus();

    const saveBtn = document.createElement('button');
    saveBtn.textContent = '保存';
    saveBtn.style.cssText = 'margin-top:6px;padding:6px 16px;background:var(--accent);color:#fff;border:none;border-radius:40px;cursor:pointer;font-size:0.8rem;';
    bubble.appendChild(saveBtn);

    const cancelBtn = document.createElement('button');
    cancelBtn.textContent = '取消';
    cancelBtn.style.cssText = 'margin-top:6px;margin-left:6px;padding:6px 16px;background:var(--border);color:var(--text2);border:none;border-radius:40px;cursor:pointer;font-size:0.8rem;';
    bubble.appendChild(cancelBtn);

    const done = (save) => {
        if (save) {
            const newText = ta.value.trim();
            if (newText && newText !== originalText) {
                messages[idx] = { ...messages[idx], content: newText };
            }
        }
        msgDiv.classList.remove('editing');
        const role = messages[idx].role;
        if (role === 'ai') {
            const t = messages[idx].reasoning_content;
            updateBubble(msgDiv, messages[idx].content, t || null);
        } else {
            bubble.textContent = messages[idx].content;
        }
        autoSave();
        updateStats();
    };

    saveBtn.onclick = () => done(true);
    cancelBtn.onclick = () => done(false);
    ta.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); done(true); }
        if (e.key === 'Escape') { done(false); }
    });
}

function deleteMsg(btn) {
    const msgDiv = btn.closest('.msg');
    const mid = parseInt(msgDiv.dataset.mid);
    const idx = findMsg(mid);
    if (idx < 1) return;
    if (!confirm('删除此消息及后续所有消息？')) return;

    messages.splice(idx);
    const container = document.getElementById('messages');
    container.innerHTML = '';
    for (let i = 0; i < messages.length; i++) {
        const m = messages[i];
        if (m.role === 'system') continue;
        addMsg(m.role, m.content, m.reasoning_content, m._id);
    }
    if (!container.querySelector('.msg')) {
        container.innerHTML = '<div class="empty-state">💬 消息已清空，开始新对话</div>';
    }
    autoSave();
    updateStats();
}

function forkFrom(btn) {
    const msgDiv = btn.closest('.msg');
    const mid = parseInt(msgDiv.dataset.mid);
    const idx = findMsg(mid);
    if (idx < 1) return;

    messages.splice(idx + 1);
    const container = document.getElementById('messages');
    container.innerHTML = '';
    for (let i = 0; i < messages.length; i++) {
        const m = messages[i];
        if (m.role === 'system') continue;
        addMsg(m.role, m.content, m.reasoning_content, m._id);
    }
    if (!container.querySelector('.msg')) {
        container.innerHTML = '<div class="empty-state">💬 消息已清空</div>';
    }
    updateStats();
    autoSave();
    toast('已从此处 fork');
}
