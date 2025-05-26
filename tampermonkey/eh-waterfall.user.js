// ==UserScript==
// @name         Waterfall View and Image Link Helper
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      25.5.26
// @description  Adds buttons for waterfall view and copying image permalinks.
// @author       Your Name
// @match        *://e-hentai.org/s/*
// @match        *://exhentai.org/s/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setClipboard
// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/eh-waterfall.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/eh-waterfall.user.js
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    // --- Create Top-Right Buttons Container ---
    const topRightContainer = document.createElement('div');
    topRightContainer.style.cssText = `
        height: auto; /* Auto height to accommodate two buttons */
        width: 100px;
        text-align: center;
        position: fixed;
        right: 20px;
        top: 20px;
        z-index: 9999; /* Ensure it's on top */
        display: flex; /* Use flex to stack buttons */
        flex-direction: column; /* Stack vertically */
        gap: 5px; /* Add some space between buttons */
    `;

    // --- Button 1: Waterfall ---
    const waterfallButton = document.createElement('button');
    waterfallButton.id = "waterfall";
    waterfallButton.textContent = "下拉式";
    waterfallButton.style.cssText = `
        width: 100%;
        height: 30px; /* Adjusted height */
        font-size: large; /* Adjusted font size */
    `;
    topRightContainer.appendChild(waterfallButton);

    // --- Button 2: Waterfall2 (Redirect) ---
    const waterfall2Button = document.createElement('button');
    waterfall2Button.id = "waterfall2";
    waterfall2Button.textContent = "新页面"; // Changed text for clarity
    waterfall2Button.style.cssText = `
        width: 100%;
        height: 30px; /* Adjusted height */
        font-size: large; /* Adjusted font size */
    `;
    topRightContainer.appendChild(waterfall2Button);

    document.body.appendChild(topRightContainer);

    // --- Create Top-Left Button Container ---
    const topLeftContainer = document.createElement('div');
    topLeftContainer.style.cssText = `
        height: 60px;
        width: 100px;
        text-align: center;
        position: fixed;
        left: 20px;
        top: 20px;
        z-index: 9999; /* Ensure it's on top */
    `;

    // --- Button 3: Origin Button (Copy Link) ---
    const originButton = document.createElement('button');
    originButton.id = "originBtn";
    originButton.textContent = "复制图片外链";
    originButton.style.cssText = `
        width: 100%;
        height: 100%;
        font-size: large; /* Adjusted font size, x-large can be very big */
    `;
    topLeftContainer.appendChild(originButton);
    document.body.appendChild(topLeftContainer);


    // --- JavaScript Functions ---

    async function execWaterfall() {
        console.log('Executing Waterfall!');
        if (document.getElementById("originBtn")) document.getElementById("originBtn").remove();
        if (document.getElementById("waterfall")) document.getElementById("waterfall").remove();
        if (document.getElementById("waterfall2")) document.getElementById("waterfall2").remove();
        // Optionally remove the containers as well
        if (topRightContainer.parentNode) topRightContainer.remove();
        if (topLeftContainer.parentNode) topLeftContainer.remove();


        let pn = document.createElement('div');
        pn.style.textAlign = 'center'; // Center images

        const targetElement = document.getElementById('i1'); // Element to append images
        if (!targetElement) {
            console.error("Element with id 'i1' not found for waterfall.");
            alert("Waterfall target element 'i1' not found!");
            return;
        }
        // Clear target element and append new container
        targetElement.innerHTML = '';
        targetElement.appendChild(pn);

        let ln = location.href; // Last successful URL
        let hnElement = document.getElementById('next'); // Get the 'next' link element
        let hn = hnElement ? hnElement.href : null; // Initial next href

        while (hn && hn !== ln) { // Loop while there's a next link and it's different
            try {
                const htmlText = await new Promise((resolve, reject) => {
                    console.log("Fetching:", hn);
                    GM_xmlhttpRequest({
                        method: "GET",
                        url: hn,
                        onload: function(response) {
                            if (response.status >= 200 && response.status < 400) {
                                resolve(response.responseText);
                            } else {
                                reject(new Error(`Failed to fetch ${hn}. Status: ${response.status}`));
                            }
                        },
                        onerror: function(response) {
                            reject(new Error(`Error fetching ${hn}: ${response.statusText || 'Network error'}`));
                        },
                        ontimeout: function() {
                            reject(new Error(`Timeout fetching ${hn}`));
                        }
                    });
                });

                let parser = new DOMParser();
                let doc = parser.parseFromString(htmlText, "text/html");
                console.log("Parsed document from:", hn);

                let imgElement = doc.getElementById('img');
                let nextElementOnFetchedPage = doc.getElementById('next');

                if (imgElement && imgElement.src) {
                    let img = document.createElement('img');
                    img.src = imgElement.src;
                    img.style.maxWidth = '100%'; // Make images responsive
                    img.style.height = 'auto';
                    img.style.display = 'block'; // Ensure it takes its own line
                    img.style.margin = '10px auto'; // Add some margin
                    pn.appendChild(img);
                    ln = hn; // Update last successful URL
                } else {
                    console.warn("Image element 'img' not found or no src in fetched page:", hn);
                    // Optionally break or try to find image differently
                }

                if (nextElementOnFetchedPage && nextElementOnFetchedPage.href) {
                    hn = nextElementOnFetchedPage.href;
                } else {
                    console.log("No 'next' link found on fetched page:", hn);
                    hn = null; // Stop loop if no next link
                }

            } catch (error) {
                console.error("Error in waterfall loop for URL:", hn, error);
                alert(`Error fetching page: ${hn}\n${error.message}`);
                hn = null; // Stop loop on error
            }
        }
        console.log("Waterfall finished or no more pages.");
        let p = document.createElement('p');
        p.innerHTML = "End of content or last page: " + ln;
        pn.appendChild(p);
    }

    async function execWaterfall2() {
        const currentPath = window.location.pathname + window.location.search + window.location.hash; // Include query and hash
        const newUrl = 'https://page.moonchan.xyz/#' + currentPath;
        window.location.href = newUrl;
    }

    // --- Event Listeners ---
    if (waterfallButton) {
        waterfallButton.addEventListener("click", execWaterfall, false);
    }
    if (waterfall2Button) {
        waterfall2Button.addEventListener("click", execWaterfall2, false);
    }
    if (originButton) {
        originButton.addEventListener("click", function() {
            const currentUrl = window.location.href;
            const hasQuery = currentUrl.includes('?');
            const newUrl = currentUrl + (hasQuery ? '&' : '?') + 'redirect_to=image';

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(newUrl)
                    .then(() => alert('已复制到剪贴板！\n' + newUrl))
                    .catch((err) => {
                        console.warn("navigator.clipboard.writeText failed, trying fallback. Error:", err);
                        fallbackCopy(newUrl);
                    });
            } else {
                fallbackCopy(newUrl);
            }
        });
    }

    function fallbackCopy(text) {
        try {
            // Try GM_setClipboard first if available and granted
            if (typeof GM_setClipboard !== 'undefined') {
                GM_setClipboard(text);
                alert('已复制 (GM_setClipboard):\n' + text);
                return;
            }
        } catch (e) {
            console.warn("GM_setClipboard failed or not available:", e);
        }

        // Original textarea fallback
        const input = document.createElement('textarea'); // Use textarea for multi-line, though URL is single
        input.value = text;
        input.style.position = 'fixed'; // Prevent scrolling to bottom
        input.style.left = '-9999px';
        document.body.appendChild(input);
        input.select();
        input.setSelectionRange(0, 99999); // For mobile browsers

        try {
            const successful = document.execCommand('copy');
            if (successful) {
                alert('已复制 (兼容模式):\n' + text);
            } else {
                alert('复制失败，请手动复制。');
            }
        } catch (err) {
            console.error('Fallback copy error:', err);
            alert('复制失败，请手动复制。');
        } finally {
            document.body.removeChild(input);
        }
    }

    console.log("Waterfall/Helper buttons added.");

})();