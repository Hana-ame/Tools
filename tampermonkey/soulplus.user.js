// ==UserScript==
// @name         Soul-Plus
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      25.4.14
// @description  全都通到一个网址
// @match        *://*.white-plus.net/*
// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/soulplus.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/soulplus.user.js
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    window.location.hostname = "soul-plus.org"
})();