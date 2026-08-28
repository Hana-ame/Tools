// ==UserScript==
// @name         YouTube倍速控制器
// @namespace    https://github.com/Hana-ame/Tools/tree/tampermonkey
// @version      26.8.28
// @description  支持任意倍率调节的YouTube播放控制，快捷键+预设+记忆+悬浮球 (修复TrustedHTML，悬浮球移至右上角)
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
    const BALL_KEY = 'yt_ball_pos';

    const getVideo = () => document.querySelector('video');
    const loadSpeed = () => parseFloat(localStorage.getItem(LS_KEY)) || 1;
    const saveSpeed = (v) => localStorage.setItem(LS_KEY, v);
    const loadJSON = (key) => { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } };
    const saveJSON = (key, obj) => localStorage.setItem(key, JSON.stringify(obj));

    let currentSpeed = loadSpeed();
    const savedPos = loadJSON(POS_KEY);
    const savedBall = loadJSON(BALL_KEY);

    // ======================== 面板 ========================
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

    const titleText = document.createTextNode('倍速 ');
    const speedDisplay = document.createElement('span');
    speedDisplay.id = 'yt-speed-display';
    speedDisplay.style.cssText = 'color:#ff4444;font-weight:700;font-size:15px';
    speedDisplay.textContent = currentSpeed.toFixed(1) + 'x';

    header.appendChild(titleText);
    header.appendChild(speedDisplay);

    // ---------- 拖拽（面板） ----------
    let drag = false, dragStartX, dragStartY, dragOrigX, dragOrigY;
    const onDragStart = (e) => {
        if (e.target.tagName === 'BUTTON') return;
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
        saveJSON(POS_KEY, { x: rect.left, y: rect.top });
    };
    header.addEventListener('mousedown', onDragStart);
    document.addEventListener('mousemove', onDragMove);
    document.addEventListener('mouseup', onDragEnd);

    // ---------- 预设按钮 ----------
    const presetsRow = document.createElement('div');
    presetsRow.style.cssText = 'display:flex;gap:4px;flex-wrap:wrap;';

    const presets = [1, 1.5, 2, 2.5, 3];

    const updateDisplay = () => {
        const el = document.getElementById('yt-speed-display');
        if (el) el.textContent = currentSpeed.toFixed(1) + 'x';
        ballLabel.textContent = currentSpeed.toFixed(1) + 'x';
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

    // ---------- 自定义输入 ----------
    const customRow = document.createElement('div');
    customRow.style.cssText = 'display:flex;gap:4px;';

    const input = document.createElement('input');
    input.type = 'number';
    input.placeholder = '自定义';
    input.min = 0.1; input.max = 16; input.step = 0.1;
    input.value = currentSpeed;
    input.style.cssText = `
        flex:1; padding:4px 6px; border:1px solid rgba(255,255,255,.15);
        border-radius:4px; background:rgba(255,255,255,.06);
        color:#fff; font-size:12px; outline:none; width:60px;
    `;

    const applyBtn = document.createElement('button');
    applyBtn.textContent = '✓';
    applyBtn.style.cssText = `
        padding:4px 10px; border:none; border-radius:4px;
        background:#ff4444; color:#fff; cursor:pointer;
        font-size:13px; font-weight:700;
    `;
    applyBtn.onclick = () => setRate(parseFloat(input.value) || 1);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') setRate(parseFloat(input.value) || 1);
    });

    customRow.appendChild(input);
    customRow.appendChild(applyBtn);

    // ---------- 关闭按钮 ----------
    const closeBtn = document.createElement('button');
    closeBtn.textContent = '✕';
    closeBtn.style.cssText = `
        background:none; border:none; color:#888; cursor:pointer;
        font-size:14px; padding:0 2px;
    `;
    closeBtn.onclick = () => {
        container.style.display = 'none';
        ball.style.display = 'flex';
    };
    header.appendChild(closeBtn);

    container.appendChild(header);
    container.appendChild(presetsRow);
    container.appendChild(customRow);
    document.body.appendChild(container);

    // ======================== 悬浮球 ========================
    const ball = document.createElement('div');
    ball.style.cssText = `
        position: fixed; z-index: 9998;
        width: 46px; height: 46px; border-radius: 50%;
        background: rgba(28,28,28,0.92); backdrop-filter: blur(4px);
        border: 2px solid rgba(255,68,68,0.6);
        display: none; justify-content: center; align-items: center;
        cursor: pointer; user-select: none; touch-action: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
        ${savedBall ? `left:${savedBall.x}px;top:${savedBall.y}px` : 'top:70px;right:16px'};
        transition: opacity .2s, transform .15s;
    `;

    const ballLabel = document.createElement('span');
    ballLabel.style.cssText = `
        color: #ff4444; font-weight: 700; font-size: 12px;
        font-family: Roboto,Arial,sans-serif; pointer-events: none;
    `;
    ballLabel.textContent = currentSpeed.toFixed(1) + 'x';
    ball.appendChild(ballLabel);
    document.body.appendChild(ball);

    // 悬浮球拖拽（鼠标 + 触摸）
    let ballDrag = false, ballMoved = false;
    let bStartX, bStartY, bOrigX, bOrigY;

    const onBallStart = (e) => {
        ballDrag = true; ballMoved = false;
        const rect = ball.getBoundingClientRect();
        const pt = e.touches ? e.touches[0] : e;
        bStartX = pt.clientX; bStartY = pt.clientY;
        bOrigX = rect.left; bOrigY = rect.top;
        ball.style.transition = 'none';
        ball.style.right = 'auto'; ball.style.bottom = 'auto';
    };
    const onBallMove = (e) => {
        if (!ballDrag) return;
        const pt = e.touches ? e.touches[0] : e;
        const dx = pt.clientX - bStartX, dy = pt.clientY - bStartY;
        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) ballMoved = true;
        ball.style.left = (bOrigX + dx) + 'px';
        ball.style.top = (bOrigY + dy) + 'px';
    };
    const onBallEnd = () => {
        if (!ballDrag) return;
        ballDrag = false;
        ball.style.transition = 'opacity .2s, transform .15s';
        const rect = ball.getBoundingClientRect();
        saveJSON(BALL_KEY, { x: rect.left, y: rect.top });
        if (!ballMoved) {
            container.style.display = 'flex';
            ball.style.display = 'none';
        }
    };

    ball.addEventListener('mousedown', onBallStart);
    document.addEventListener('mousemove', onBallMove);
    document.addEventListener('mouseup', onBallEnd);
    ball.addEventListener('touchstart', onBallStart, { passive: true });
    document.addEventListener('touchmove', onBallMove, { passive: true });
    document.addEventListener('touchend', onBallEnd);

    // ======================== 同步视频倍速 ========================
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

    // ======================== 键盘快捷键（桌面端） ========================
    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        if (e.key === '[') { e.preventDefault(); setRate(currentSpeed - 0.25); }
        else if (e.key === ']') { e.preventDefault(); setRate(currentSpeed + 0.25); }
        else if (e.key === '\\') { e.preventDefault(); setRate(1); }
    });

    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            if (container.style.display === 'none') {
                container.style.display = 'flex'; ball.style.display = 'none';
            } else {
                container.style.display = 'none'; ball.style.display = 'flex';
            }
        }
    });
})();
