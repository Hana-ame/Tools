// ==UserScript==
// @name         bilibili倍速
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      1.0
// @description  添加倍速选项
// @match        *://*.bilibili.com/*
// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/bilibili.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/bilibili.user.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 目标倍速列表（可自由修改）
    const customRates = [1.75, 2.0, 2.5, 3.0];
    
    // 等待DOM加载完成
    window.addEventListener('DOMContentLoaded', function() {
        const observer = new MutationObserver(function(mutations) {
            // 定位倍速菜单容器
            const rateMenu = document.querySelector('.bpx-player-ctrl-playbackrate-menu');
            
            if (rateMenu) {
                // 清空现有倍速选项（可选）
                // rateMenu.innerHTML = '';

                // 创建自定义倍速项
                customRates.forEach(rate => {
                    const li = document.createElement('li');
                    li.className = 'bpx-player-ctrl-playbackrate-menu-item';
                    li.dataset.value = rate;
                    li.textContent = `${rate}x`;

                    rateMenu.appendChild(li);
                });

                // 停止观察
                observer.disconnect();
            }
        });

        // 开始监控DOM变化[3](@ref)
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
})();