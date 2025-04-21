// ==UserScript==
// @name         bilibili倍速
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      25.4.22
// @description  添加倍速选项
// @match        *://*.bilibili.com/*
// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/bilibili.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/bilibili.user.js
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    const addMoreRates = () => {
        // 目标倍速列表（可自由修改）
        const customRates = [1, 1.5, 2, 2.5, 3, 3.5];
        let rateMenu = document.querySelector('.bpx-player-ctrl-playbackrate-menu');
        console.log(rateMenu);

        if (rateMenu == null) {
            setTimeout(() => { addMoreRates(); }, 1000);
            return;
        }

        if (rateMenu) {
            // 清空现有倍速选项（可选）
            rateMenu.innerHTML = '';

            // 创建自定义倍速项
            customRates.forEach(rate => {
                const li = document.createElement('li');
                li.className = 'bpx-player-ctrl-playbackrate-menu-item';
                li.dataset.value = rate;
                li.textContent = `${rate}x`;

                rateMenu.appendChild(li);
            });
        }
    }

    window.onload = () => {
        // 等待页面加载完成
        setTimeout(() => {
            addMoreRates();
        }, 1000); // 延迟1秒以确保元素加载完成
    };
})();