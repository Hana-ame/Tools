// ==UserScript==
// @name         YouTube倍速控制器
// @namespace    https://github.com/Hana-ame/Tools/tree/tampermonkey
// @version      26.7.24
// @description  支持任意倍率调节的YouTube播放控制，快捷键+预设+记忆
// @match        *://www.youtube.com/*
// @match        *://m.youtube.com/*
// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/tampermonkey/youtube.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/tampermonkey/youtube.user.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const LS_KEY = 'yt_speed_value';
    const POS_KEY = 'yt_panel_pos';

    const getVideo = () => document.querySelector('video');
    const loadSpeed = () => parseFloat(localStorage.getItem(LS_KEY)) || 1;
    const saveSpeed = (v) => localStorage.setItem(LS_KEY, v);
    const loadPos = () => { try { return JSON.parse(localStorage.getItem(POS_KEY)); } catch { return null; } };
    const savePos = (x, y) => localStorage.setItem(POS_KEY, JSON.stringify({ x, y }));

    let currentSpeed = loadSpeed();
    const savedPos = loadPos();

    const container = document.createElement('div');
    container.style.cssText = `
        position: fixed; z-index: 9999;
        background: rgba(28,28,28,0.92); border-radius: 8px;
        padding: 10px 14px; display: flex; flex-direction: column;
        gap: 6px; font-family: Roboto,Arial,sans-serif;
        min-width: 140px; backdrop-filter: blur(4px);
        ${savedPos ? `left:${savedPos.x}px;top:${savedPos.y}px` : 'top:60px;right:20px'};
        transition: opacity .2s;
    `;

    const header = document.createElement('div');
    header.style.cssText = `
        display: flex; justify-content: space-between; align-items: center;
        color: #fff; font-size: 13px; font-weight: 500;
        cursor: move; user-select: none;
    `;
    header.innerHTML = '倍速 <span id="yt-speed-display" style="color:#ff4444;font-weight:700;font-size:15px">1.0x</span>';

    let drag = false, dragStartX, dragStartY, dragOrigX, dragOrigY;
    const onDragStart = (e) => {
        drag = true;
        const rect = container.getBoundingClientRect();
        dragStartX = e.clientX; dragStartY = e.clientY;
        dragOrigX = rect.left; dragOrigY = rect.top;
        container.style.transition = 'none';
        container.style.right = 'auto';
    };
    const onDragMove = (e) => {
        if (!drag) return;
        const dx = e.clientX - dragStartX, dy = e.clientY - dragStartY;
        container.style.left = (dragOrigX + dx) + 'px';
        container.style.top = (dragOrigY + dy) + 'px';
    };
    const onDragEnd = () => {
        if (!drag) return;
        drag = false;
        container.style.transition = 'opacity .2s';
        const rect = container.getBoundingClientRect();
        savePos(rect.left, rect.top);
    };
    header.addEventListener('mousedown', onDragStart);
    document.addEventListener('mousemove', onDragMove);
    document.addEventListener('mouseup', onDragEnd);

    const presetsRow = document.createElement('div');
    presetsRow.style.cssText = `
        display: flex; gap: 4px; flex-wrap: wrap;
    `;

    const presets = [1, 1.5, 2, 2.5, 3];

    const updateDisplay = () => {
        const el = document.getElementById('yt-speed-display');
        if (el) el.textContent = currentSpeed.toFixed(1) + 'x';
    };

    const setRate = (rate) => {
        currentSpeed = Math.max(0.1, Math.min(16, rate));
        saveSpeed(currentSpeed);
        updateDisplay();
        const v = getVideo();
        if (v) v.playbackRate = currentSpeed;
    };

    presets.forEach(r => {
        const btn = document.createElement('button');
        btn.textContent = r + 'x';
        btn.style.cssText = `
            padding: 4px 10px; border: 1px solid rgba(255,255,255,.15);
            border-radius: 4px; background: rgba(255,255,255,.08);
            color: #eee; cursor: pointer; font-size: 12px;
            transition: background .15s;
        `;
        btn.onmouseenter = () => btn.style.background = 'rgba(255,255,255,.18)';
        btn.onmouseleave = () => btn.style.background = 'rgba(255,255,255,.08)';
        btn.onclick = () => setRate(r);
        presetsRow.appendChild(btn);
    });

    const customRow = document.createElement('div');
    customRow.style.cssText = `display: flex; gap: 4px;`;

    const input = document.createElement('input');
    input.type = 'number';
    input.placeholder = '自定义';
    input.min = 0.1;
    input.max = 16;
    input.step = 0.1;
    input.value = currentSpeed;
    input.style.cssText = `
        flex: 1; padding: 4px 6px; border: 1px solid rgba(255,255,255,.15);
        border-radius: 4px; background: rgba(255,255,255,.06);
        color: #fff; font-size: 12px; outline: none; width: 60px;
    `;

    const applyBtn = document.createElement('button');
    applyBtn.textContent = '✓';
    applyBtn.style.cssText = `
        padding: 4px 10px; border: none; border-radius: 4px;
        background: #ff4444; color: #fff; cursor: pointer;
        font-size: 13px; font-weight: 700;
    `;
    applyBtn.onclick = () => setRate(parseFloat(input.value) || 1);

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') setRate(parseFloat(input.value) || 1);
    });

    customRow.appendChild(input);
    customRow.appendChild(applyBtn);

    const closeBtn = document.createElement('button');
    closeBtn.textContent = '✕';
    closeBtn.style.cssText = `
        background: none; border: none; color: #888; cursor: pointer;
        font-size: 14px; padding: 0 2px;
    `;
    closeBtn.onclick = () => container.style.display = 'none';
    header.appendChild(closeBtn);

    container.appendChild(header);
    container.appendChild(presetsRow);
    container.appendChild(customRow);
    document.body.appendChild(container);

    updateDisplay();

    const applyToVideo = () => {
        const v = getVideo();
        if (v && Math.abs(v.playbackRate - currentSpeed) > 0.01) {
            v.playbackRate = currentSpeed;
        }
    };

    applyToVideo();
    const observer = new MutationObserver(applyToVideo);
    observer.observe(document.body, { childList: true, subtree: true, attributes: false });

    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.key === '[') {
            e.preventDefault();
            setRate(currentSpeed - 0.25);
        } else if (e.key === ']') {
            e.preventDefault();
            setRate(currentSpeed + 0.25);
        } else if (e.key === '\\') {
            e.preventDefault();
            setRate(1);
        }
    });

    const togglePanel = () => {
        container.style.display = container.style.display === 'none' ? 'flex' : 'none';
    };

    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            togglePanel();
        }
    });
})();
