// ==UserScript==
// @name         Remove Logo-BG Elements
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      25.5.3
// @description  去除所有包含 logo-bg 类名的元素样式
// @match        https://i.jandan.net/*

// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/jandan.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/jandan.user.js
// @grant        GM_addStyle

// ==/UserScript==

(function() {
    'use strict';

    // 方式1：直接清除现有元素的 class 和 style
    function removeLogoBg() {
        document.querySelectorAll('[class*="logo-bg"]').forEach(element => {
            // 移除 logo-bg 类名
            element.classList.remove('logo-bg');
            // 清空内联样式
            element.style.cssText = '';
        });
    }

    // 方式2：通过 CSS 覆盖样式（防止动态加载）
    GM_addStyle(`
        [class*="logo-bg"] {
            background-image: none !important;
            display: none !important;
            /* 添加其他需要重置的样式 */
        }
    `);

    // 初始化执行
    removeLogoBg();

    // 监听 DOM 变化处理动态加载的元素
    const observer = new MutationObserver(mutations => {
        mutations.forEach(() => {
            removeLogoBg();
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true
    });
})();