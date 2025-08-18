// ==UserScript==
// @name         Soul-Plus
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      25.5.3
// @description  全都通到一个网址
// @match        *://*.white-plus.net/*
// @match        *://*.north-plus.net/*
// @match        *://*.snow-plus.net/*
// @match        *://*.south-plus.net/*
// @match        *://*.south-plus.org/*
// @match        *://bbs.imoutolove.me/*
// @match        *://*.level-plus.net/*
// @match        *://*.spring-plus.net/*

// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/soulplus.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/soulplus.user.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const HOST = "south-plus.org";
    if (window.location.hostname !== HOST) window.location.hostname = HOST;

})();