function buildRequestBody() {
    const body = { messages, stream: true };
    try {
        if (params.json) {
            const extra = JSON.parse(params.json);
            Object.assign(body, extra);
        }
    } catch (e) { console.error(e); }
    delete body.timeout;
    if (!body.model) body.model = config.model;
    if (!('enable_thinking' in body) && (body.model.includes('reasoner') || body.model.includes('deepseek-v4'))) {
        body.enable_thinking = true;
    }
    return body;
}

async function send() {
    try {
        const input = document.getElementById('input');
        const text = input.value.trim();
        if (!text || loading) return;

        if (!config.key) { showConfig(); return; }

        input.value = '';
        input.style.height = 'auto';
        const userMid = nextId();
        messages.push({ role: 'user', content: text, _id: userMid });
        const userDiv = addMsg('user', text, null, userMid);
        const pendingBadge = document.createElement('span');
        pendingBadge.className = 'pending-badge';
        pendingBadge.textContent = ' ⏳';
        pendingBadge.style.cssText = 'font-size:0.75rem;opacity:0.6;';
        userDiv.querySelector('.bubble').appendChild(pendingBadge);
        loading = true;
        document.getElementById('sendBtn').disabled = true;

        const aiMid = nextId();
        const aiIdx = messages.length;
        messages.push({ role: 'assistant', content: '', _id: aiMid });
        const msgDiv = addMsg('ai', '...', null, aiMid);
        msgDiv.classList.add('typing');
        let fullContent = '';
        let fullReasoning = '';

        try {
            const body = buildRequestBody();
            let timeoutMs = 120000;
            try { const p = JSON.parse(params.json); if (p.timeout > 0) timeoutMs = p.timeout * 1000; } catch {}
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), timeoutMs);
            const resp = await fetch(config.url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${config.key}`
                },
                body: JSON.stringify(body),
                signal: controller.signal
            });
            clearTimeout(timer);

            if (!resp.ok) {
                const err = await resp.text();
                throw new Error(`HTTP ${resp.status}: ${err}`);
            }

            msgDiv.classList.remove('typing');
            pendingBadge.remove();
            const reader = resp.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed || !trimmed.startsWith('data: ')) continue;
                    const data = trimmed.slice(6).trim();
                    if (data === '[DONE]') continue;
                    try {
                        const json = JSON.parse(data);
                        const choices = json.choices;
                        if (!choices || !choices.length) continue;
                        const delta = choices[0].delta;
                        if (delta.reasoning_content) fullReasoning += delta.reasoning_content;
                        if (delta.content) fullContent += delta.content;
                        updateBubble(msgDiv, fullContent, fullReasoning || null);
                    } catch (e) { console.error(e); }
                }
            }

            if (buffer.trim()) {
                const data = buffer.trim().slice(6).trim();
                if (data !== '[DONE]') {
                    try {
                        const json = JSON.parse(data);
                        const delta = json.choices?.[0]?.delta;
                        if (delta?.reasoning_content) fullReasoning += delta.reasoning_content;
                        if (delta?.content) fullContent += delta.content;
                        updateBubble(msgDiv, fullContent, fullReasoning || null);
                    } catch (e) { console.error(e); }
                }
            }

            messages[aiIdx] = { _id: aiMid, role: 'assistant', content: fullContent, reasoning_content: fullReasoning || undefined };
            updateStats();
            autoSave();

        } catch (e) {
            console.error(e);
            msgDiv.classList.remove('typing');
            if (pendingBadge.parentNode) pendingBadge.remove();
            const bubble = msgDiv.querySelector('.bubble');
            if (bubble) bubble.innerHTML = `<span style="color:#dc2626">❌ ${e.message}</span>`;
        }
    } catch (e) {
        console.error('send outer error:', e);
    } finally {
        loading = false;
        document.getElementById('sendBtn').disabled = false;
    }
}

function onKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
}
