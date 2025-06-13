// ==UserScript==
// @name         quick poster
// @namespace    https://github.com/Hana-ame/Tools/tree/master/tampermonkey
// @version      0.8
// @description
// @author       You
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @connect      *
// @connect      moonchan.xyz
// @updateURL    https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/quickPost.user.js
// @downloadURL  https://raw.githubusercontent.com/Hana-ame/Tools/refs/heads/master/tampermonkey/quickPost.user.js
// @run-at       document-idle
// ==/UserScript==

(function () {
    'use strict';

    function getProxiedImageUrl(imageUrl) {
        try {
            // 1. 解析原始 URL
            const originalUrl = new URL(imageUrl);
            const originalHost = originalUrl.hostname; // e.g., "ww1.sinaimg.cn"

            // 2. 检查 host domain 是否是 *.sinaimg.cn
            if (originalHost.endsWith('.sinaimg.cn')) {
                // 3. 构建新的 URL
                // 新的 host
                const newHost = 'proxy.moonchan.xyz';

                // 保留原始的 protocol, pathname, hash
                // 注意: 如果原始 URL 有 searchParams，这里会丢弃它们，只添加新的 proxy 参数。
                // 如果需要保留原始 searchParams，需要额外处理。
                // 对于图片 URL，通常 searchParams 不太重要，或者代理服务会处理路径。

                const proxiedUrl = new URL(originalUrl.pathname, `https://${newHost}`); // 使用 https 作为新协议

                // 4. 添加 searchParams
                proxiedUrl.searchParams.set('proxy_host', originalHost);
                proxiedUrl.searchParams.set('proxy_referer', 'https://weibo.com/');

                return proxiedUrl.toString();
            } else {
                // 如果不匹配，返回原始 URL
                return imageUrl;
            }
        } catch (error) {
            // 如果 URL 无效或发生其他错误，打印错误并返回原始 URL
            console.error("Error processing URL:", imageUrl, error);
            return imageUrl;
        }
    }


    // Function to execute when the button is clicked
    function postImageData(imgElement, id) {
        if (!imgElement || !imgElement.src) {
            console.log('Could not find the image or its src attribute.');
            alert('Could not find the image or its src attribute.');
            return;
        }

        const imageUrl = imgElement.src;

        const apiUrl = `https://moonchan.xyz/api/v2/?bid=${id}`;
        const headers = {
            "Content-Type": "application/json"
        };
        const bodyPayload = {
            p: getProxiedImageUrl(imageUrl),
            txt: "无文本"
        };

        console.log("Sending POST request to:", apiUrl);
        console.log("With headers:", headers);
        console.log("With JSON body:", bodyPayload);

        GM_xmlhttpRequest({
            method: "POST",
            url: apiUrl,
            headers: headers,
            data: JSON.stringify(bodyPayload), // 'data' for GM_xmlhttpRequest, not 'body'
            credentials: 'include',
            // for fetch is somewhat analogous to GM_xmlhttpRequest
            // sending cookies for the target domain by default. If the API relies on
            // cookies set by moonchan.xyz, they should be included.
            // If you need to ensure cookies from the *current* page's domain are NOT sent,
            // or if you need fine-grained control, check GM_xmlhttpRequest options like 'anonymous'.
            // For most simple POSTs like this, the default behavior regarding cookies is often sufficient.

            onload: function (response) {
                console.log('GM_xmlhttpRequest Success:');
                console.log('Status:', response.status);
                console.log('Response Text:', response.responseText);
                try {
                    const responseData = JSON.parse(response.responseText);
                    console.log('Parsed Response Data:', responseData);
                    alert('Data sent successfully!\nStatus: ' + response.status + '\nResponse: ' + response.responseText);
                } catch (e) {
                    console.warn('Response was not valid JSON:', response.responseText);
                }
            },
            onerror: function (response) {
                console.error('GM_xmlhttpRequest Error:');
                console.log('Status:', response.status);
                console.log('Status Text:', response.statusText);
                console.log('Response Headers:', response.responseHeaders);
                console.log('Response Text:', response.responseText);
                alert(`Failed to send data.\nStatus: ${response.status} ${response.statusText}\nError: ${response.responseText}`);
            },
            ontimeout: function () {
                console.error('GM_xmlhttpRequest Timeout');
                alert('Request timed out.');
            }
        });
    }

    // Function to execute when the button is clicked
    function logImageSrc(imgElement) {
        if (imgElement && imgElement.src) {
            console.log('Image Src:', imgElement.src);
            // 你也可以在这里添加一个alert或者其他用户反馈
            // alert('Image source logged to console: ' + imgElement.src);
        } else {
            console.log('Could not find the image or its src attribute.');
        }
    }

    // Wait for the page to be somewhat settled
    // @run-at document-idle helps with this, but a small delay can sometimes be beneficial for dynamic content
    // For this specific simple check, it's often fine without an explicit timeout.

    // Check the number of <img> tags within the <body>
    const imagesInBody = document.body.getElementsByTagName('img');
    const elemsInBody = document.body.getElementsByTagName('*');
    if (imagesInBody.length === 1 && elemsInBody.length === 1) {
        const singleImageElement = imagesInBody[0];

        function appendButton(text, id, top) {
            // Create the button
            const button = document.createElement('button');
            button.textContent = text;

            // Style the button
            button.style.position = 'fixed';
            button.style.top = top;
            button.style.right = '10px';
            button.style.zIndex = '99999'; // Ensure it's on top
            button.style.padding = '8px 12px';
            button.style.backgroundColor = '#4CAF50'; // A pleasant green
            button.style.color = 'white';
            button.style.border = 'none';
            button.style.borderRadius = '4px';
            button.style.cursor = 'pointer';
            button.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';

            // Add event listener to the button
            button.addEventListener('click', function () {
                postImageData(singleImageElement, id); // Pass the found image element
            });

            // Append the button to the body
            document.body.appendChild(button);
        }
        appendButton("串", 12, '10px');
        appendButton("打捞", 23, '60px');
        appendButton("10001", 10001, '100px');
        appendButton("色图", 103, '140px');

        console.log('Single Image Src Logger: Button added for the image.');

    } else {
        // Optional: Log if the condition is not met (for debugging purposes)
        // console.log('Single Image Src Logger: Not a single image page. Images found: ' + imagesInBody.length);
    }
})();