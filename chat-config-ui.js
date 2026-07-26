function showConfig() {
    document.getElementById('cfgUrl').value = config.url;
    document.getElementById('cfgKey').value = config.key;
    document.getElementById('cfgModel').value = config.model;
    document.getElementById('cfgSystem').value = config.system;
    showModal('configModal');
}

function showParams() {
    switchParamMode(params.mode);
    showModal('paramsModal');
}

function jsonToRows(jsonStr) {
    let obj = {};
    try { obj = JSON.parse(jsonStr); } catch (e) { console.error(e); }
    const rows = [];
    for (const [key, val] of Object.entries(obj)) {
        rows.push({ key, value: JSON.stringify(val), enabled: true, locked: true });
    }
    return rows;
}

function rowsToJson(rows) {
    const obj = {};
    for (const r of rows) {
        if (!r.enabled) continue;
        try { obj[r.key] = JSON.parse(r.value); } catch (e) { console.error(e); obj[r.key] = r.value; }
    }
    return JSON.stringify(obj, null, 2);
}

function renderParamTable(rows) {
    const container = document.getElementById('paramRows');
    container.innerHTML = '';
    for (let i = 0; i < rows.length; i++) {
        const r = rows[i];
        const div = document.createElement('div');
        div.className = 'param-row';
        div.dataset.idx = i;

        const chk = document.createElement('input');
        chk.type = 'checkbox';
        chk.className = 'p-chk';
        chk.checked = r.enabled;
        chk.onchange = () => { r.enabled = chk.checked; };
        div.appendChild(chk);

        let keyEl;
        if (r.locked) {
            keyEl = document.createElement('span');
            keyEl.className = 'p-key locked';
            keyEl.textContent = r.key;
        } else {
            keyEl = document.createElement('input');
            keyEl.className = 'p-key';
            keyEl.type = 'text';
            keyEl.value = r.key;
            keyEl.placeholder = 'key';
            keyEl.style.cssText = 'font-size:0.82rem;font-weight:600;color:#374151;min-width:100px;font-family:"SF Mono",Consolas,monospace;border:1px solid #d1d5db;border-radius:6px;padding:4px 6px;outline:none;';
            keyEl.oninput = () => { r.key = keyEl.value; };
        }
        div.appendChild(keyEl);

        const valWrap = document.createElement('div');
        valWrap.className = 'p-val';
        const inp = document.createElement('input');
        inp.type = 'text';
        inp.value = r.value;
        inp.placeholder = 'value';
        inp.style.cssText = 'width:100%;padding:6px 8px;border:1px solid #d1d5db;border-radius:8px;font-size:0.82rem;outline:none;font-family:"SF Mono",Consolas,monospace;';
        inp.oninput = () => { r.value = inp.value; };
        valWrap.appendChild(inp);
        div.appendChild(valWrap);

        if (!r.locked) {
            const del = document.createElement('button');
            del.className = 'p-del';
            del.textContent = '✕';
            del.onclick = () => {
                rows.splice(i, 1);
                renderParamTable(rows);
            };
            div.appendChild(del);
        }

        container.appendChild(div);
    }
    const addBtn = document.createElement('button');
    addBtn.className = 'hdr-btn';
    addBtn.textContent = '+ 添加字段';
    addBtn.style.cssText = 'margin-top:6px;';
    addBtn.onclick = () => {
        rows.push({ key: '', value: '', enabled: true, locked: false });
        renderParamTable(rows);
        const allRows = container.querySelectorAll('.param-row');
        const last = allRows[allRows.length - 1];
        if (last) { const inp = last.querySelector('input.p-key'); if (inp) inp.focus(); }
    };
    container.appendChild(addBtn);
}

function switchParamMode(mode) {
    params.mode = mode;
    document.querySelectorAll('.param-tab').forEach(t => {
        t.classList.toggle('active', t.dataset.mode === mode);
    });
    document.getElementById('paramsTableView').style.display = mode === 'table' ? '' : 'none';
    document.getElementById('paramsJsonView').style.display = mode === 'json' ? '' : 'none';

    if (mode === 'table') {
        const rows = jsonToRows(params.json);
        renderParamTable(rows);
    } else {
        document.getElementById('pJson').value = params.json;
    }
}

function saveParams() {
    if (params.mode === 'table') {
        const container = document.getElementById('paramRows');
        const rows = [];
        container.querySelectorAll('.param-row').forEach(div => {
            const idx = parseInt(div.dataset.idx);
            if (!isNaN(idx)) {
                const chk = div.querySelector('.p-chk');
                const keyEl = div.querySelector('.p-key');
                const isLocked = keyEl.classList.contains('locked');
                const valEl = div.querySelector('.p-val input, .p-val select');
                rows[idx] = {
                    key: isLocked ? keyEl.textContent : keyEl.value,
                    value: valEl ? valEl.value : '',
                    enabled: chk.checked,
                    locked: isLocked
                };
            }
        });
        params.json = rowsToJson(rows.filter(Boolean));
    } else {
        params.json = document.getElementById('pJson').value;
    }
    localStorage.setItem(PARAMS_KEY, JSON.stringify(params));
    hideModal('paramsModal');
    toast('参数已保存');
}

function resetParams() {
    params = { mode: 'table', json: paramsDefaultJson() };
    localStorage.setItem(PARAMS_KEY, JSON.stringify(params));
    switchParamMode(params.mode);
    toast('参数已重置');
}
