// ==UserScript==
// @name         bilibili倍速
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      26.7.23
// @description  添加倍速选项
// @match        *://www.bilibili.com/video/*
// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/tampermonkey/bilibili.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/tampermonkey/bilibili.user.js
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    const setRate = (rate) => {
        const video = document.querySelector('video');
        if (video) {
            video.playbackRate = rate;
            const btn = document.querySelector('.bpx-player-ctrl-playbackrate .bpx-player-ctrl-btn');
            if (btn) btn.textContent = `${rate}x`;
        }
    }

    const addMoreRates = () => {
        const customRates = [1, 1.5, 2, 2.5, 3, 3.5];
        let rateMenu = document.querySelector('.bpx-player-ctrl-playbackrate-menu');

        if (rateMenu === null) {
            setTimeout(() => { addMoreRates(); }, 1000);
            return;
        }

        rateMenu.innerHTML = '';
        customRates.forEach(rate => {
            const li = document.createElement('li');
            li.className = 'bpx-player-ctrl-playbackrate-menu-item';
            li.dataset.value = rate;
            li.textContent = `${rate}x`;
            li.addEventListener('click', (e) => {
                e.stopPropagation();
                setRate(rate);
            });
            rateMenu.appendChild(li);
        });
    }

    //window.onload = () => {
        // 等待页面加载完成
        //setTimeout(() => {
            addMoreRates();
        //}, 1000); // 延迟1秒以确保元素加载完成
    //};
})();
