// ==UserScript==
// @name         YouTube倍速控制器
// @namespace    http://tampermonkey.net/
// @version      4.0
// @description  支持任意倍率调节的YouTube播放控制
// @match        *://*.youtube.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 创建控制台标识（兼容Trusted Types）
    console.log('%c YouTube倍速控制 %c v4.0 %c',
        'background: #f44336; color: white; padding: 3px 10px;',
        'background: #4CAF50; color: white; padding: 3px 10px;',
        'color: #2196F3; font-weight: bold;');

    // 创建控制面板容器
    const controlPanel = document.createElement('div');
    controlPanel.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: rgba(255,255,255,0.9);
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        padding: 12px;
        display: flex;
        gap: 8px;
    `;

    // 创建输入框
    const speedInput = document.createElement('input');
    speedInput.type = "number";
    speedInput.placeholder = "倍速";
    speedInput.min = 0.1;
    speedInput.max = 16;
    speedInput.step = 0.1;
    speedInput.style.cssText = `
        width: 80px;
        padding: 6px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-family: Arial;
    `;

    // 创建设置按钮
    const setButton = document.createElement('button');
    setButton.textContent = "设置";
    setButton.style.cssText = `
        padding: 6px 12px;
        background: #f44336;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.3s;
    `;
    setButton.onmouseover = () => setButton.style.background = '#d32f2f';
    setButton.onmouseout = () => setButton.style.background = '#f44336';

    // 倍速设置逻辑
    const setPlaybackRate = () => {
        try {
            const speed = parseFloat(speedInput.value);
            if (isNaN(speed)) throw new Error('无效输入');

            const videos = document.getElementsByTagName('video');
            if (videos.length === 0) throw new Error('未找到视频元素');

            videos[0].playbackRate = speed;
            console.log(`成功设置倍速为: ${speed}x`);
        } catch (error) {
            alert(`错误: ${error.message}`);
        }
    };

    // 事件绑定
    setButton.onclick = setPlaybackRate;
    speedInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') setPlaybackRate();
    });

    // 组合元素
    controlPanel.appendChild(speedInput);
    controlPanel.appendChild(setButton);
    document.body.appendChild(controlPanel);
})();