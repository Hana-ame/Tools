function loadConfig() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) return JSON.parse(saved);
    } catch (e) { console.error(e); }
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
            if (p.extra) { try { Object.assign(obj, JSON.parse(p.extra)); } catch (e) { console.error(e); } }
            return { mode: 'table', json: JSON.stringify(obj, null, 2) };
        }
    } catch (e) { console.error(e); }
    return { mode: 'table', json: '{\n  "model": "deepseek-v4-flash-free",\n  "max_tokens": 8192,\n  "timeout": 120\n}' };
}

function paramsDefaultJson() {
    return '{\n  "model": "deepseek-v4-flash-free",\n  "max_tokens": 8192,\n  "timeout": 120\n}';
}

function idbConn() {
    if (_idbP) return _idbP;
    _idbP = new Promise((resolve, reject) => {
        const req = indexedDB.open('aichat_db', 1);
        req.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('conversations'))
                db.createObjectStore('conversations', { keyPath: 'id' });
        };
        req.onsuccess = (e) => { _idb = e.target.result; resolve(_idb); };
        req.onerror = (e) => { _idbP = null; reject(e.target.error); };
    });
    return _idbP;
}
function idbOp(mode, cb) {
    return idbConn().then(db => new Promise((resolve, reject) => {
        const tx = db.transaction('conversations', mode);
        const req = cb(tx.objectStore('conversations'));
        tx.oncomplete = () => resolve(req.result);
        tx.onerror = (e) => reject(e.target.error);
    }));
}
function getAllConvs() { return idbOp('readonly', s => s.getAll()); }
function putConv(d) { return idbOp('readwrite', s => s.put(d)); }
function getConvById(id) { return idbOp('readonly', s => s.get(id)); }
function deleteConvById(id) { return idbOp('readwrite', s => s.delete(id)); }

async function migrateConv() {
    try {
        const raw = localStorage.getItem(CONV_KEY);
        if (!raw) return;
        const convs = JSON.parse(raw);
        const db = await idbConn();
        const tx = db.transaction('conversations', 'readwrite');
        const store = tx.objectStore('conversations');
        for (const [id, data] of Object.entries(convs)) store.put({ ...data, id });
        await new Promise((resolve, reject) => {
            tx.oncomplete = () => { localStorage.removeItem(CONV_KEY); resolve(); };
            tx.onerror = () => reject(tx.error);
        });
        console.log('conversations migrated from localStorage to IndexedDB');
    } catch (e) { console.error('migrateConv:', e); }
}

function autoSave() {
    if (messages.length <= 1) return;
    const id = currentConvId || Date.now().toString();
    if (!currentConvId) currentConvId = id;
    putConv({ id, messages, config, params, time: Date.now() }).catch(e => console.error(e));
}
