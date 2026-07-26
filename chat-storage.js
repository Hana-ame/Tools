function loadConfig() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) return JSON.parse(saved);
    } catch {}
    return { url: 'https://zen.l.moonchan.xyz/v1/chat/completions', key: '', model: 'deepseek-v4-flash-free', system: '' };
}

function saveConfig() {
    config.url = document.getElementById('cfgUrl').value.trim();
    config.key = document.getElementById('cfgKey').value.trim();
    config.model = document.getElementById('cfgModel').value.trim();
    config.system = document.getElementById('cfgSystem').value.trim();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
    if (messages[0] && messages[0].role === 'system') {
        messages[0].content = config.system;
    } else {
        messages.unshift({ role: 'system', content: config.system });
    }
    hideModal('configModal');
    toast('设置已保存');
}

function loadParams() {
    try {
        const saved = localStorage.getItem(PARAMS_KEY);
        if (saved) {
            const p = JSON.parse(saved);
            if ('json' in p) return p;
            const obj = {};
            if (p.max_tokens) obj.max_tokens = p.max_tokens;
            if (p.temperature) obj.temperature = p.temperature;
            if (p.top_p) obj.top_p = p.top_p;
            if (p.thinking === 'true') obj.enable_thinking = true;
            else if (p.thinking === 'false') obj.enable_thinking = false;
            if (p.extra) { try { Object.assign(obj, JSON.parse(p.extra)); } catch {} }
            return { mode: 'table', json: JSON.stringify(obj, null, 2) };
        }
    } catch {}
    return { mode: 'table', json: '{\n  "model": "deepseek-v4-flash-free",\n  "max_tokens": 8192,\n  "timeout": 120\n}' };
}

function paramsDefaultJson() {
    return '{\n  "model": "deepseek-v4-flash-free",\n  "max_tokens": 8192,\n  "timeout": 120\n}';
}

function getAllConvs() {
    try {
        const raw = localStorage.getItem(CONV_KEY);
        const convs = raw ? JSON.parse(raw) : {};
        return Object.values(convs);
    } catch { return []; }
}

function putConv(d) {
    try {
        const raw = localStorage.getItem(CONV_KEY);
        const convs = raw ? JSON.parse(raw) : {};
        convs[d.id] = d;
        localStorage.setItem(CONV_KEY, JSON.stringify(convs));
    } catch (e) { toast('保存对话失败'); }
}

function getConvById(id) {
    try {
        const raw = localStorage.getItem(CONV_KEY);
        const convs = raw ? JSON.parse(raw) : {};
        return convs[id] || null;
    } catch { return null; }
}

function deleteConvById(id) {
    try {
        const raw = localStorage.getItem(CONV_KEY);
        const convs = raw ? JSON.parse(raw) : {};
        delete convs[id];
        localStorage.setItem(CONV_KEY, JSON.stringify(convs));
    } catch (e) { toast('删除对话失败'); }
}

function autoSave() {
    if (messages.length <= 1) return;
    const id = currentConvId || Date.now().toString();
    if (!currentConvId) currentConvId = id;
    putConv({ id, messages, config, params, time: Date.now() });
}
