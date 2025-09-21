// 不行，做不了。

import { useState, useEffect } from 'react';

// // 一个获取当前 location 信息的辅助函数
// function getWindowLocation() {
//   const { pathname, search, hash } = window.location;
//   // 在 Hash 模式下，我们通常关心 # 后面的部分作为路径
//   // 例如 http://example.com/#/about -> pathname 会是 '/about'
//   // 但注意：window.location.pathname 在 Hash 路由中获取到的是 # 之前的路径部分
//   // 因此，对于 Hash 路由，更常见的做法是解析 window.location.hash
//   const hashPath = window.location.hash.replace(/^#!?/, ''); // 移除开头的 # 或 #!
//   // 也可以选择使用 window.location.hash 直接包含 #
//   return {
//     // pathname: hashPath.split('?')[0] || '/', // 从哈希中提取路径部分，默认为 '/'
//     pathname,
//     search: search, // 使用 window.location 的 search
//     hash: hash, // 使用 window.location 的 hash
//     // state: null, // 简单的 Hash 路由实现可能暂不处理 state
//     // key: '', // 简单实现可能暂不生成 key
//   };
// }

// 保存原始方法
const originalPushState = window.history.pushState;
const originalReplaceState = window.history.replaceState;

// 覆写 window.history.pushState 方法
window.history.pushState = function (state, title, url) {
  const result = originalPushState.apply(this, arguments); // 调用原始方法
  // 创建并派发自定义事件 'onstatechange'
  window.dispatchEvent(new CustomEvent('onstatechange', { detail: { state, title, url } }));
  return result;
};

// 覆写 window.history.replaceState 方法
window.history.replaceState = function (state, title, url) {
  const result = originalReplaceState.apply(this, arguments); // 调用原始方法
  // 同样派发自定义事件
  window.dispatchEvent(new CustomEvent('onstatechange', { detail: { state, title, url } }));
  return result;
};

// 监听自定义的 onstatechange 事件和 popstate 事件
window.addEventListener('onstatechange', handleHistoryChange); // 程序化导航
window.addEventListener('popstate', handleHistoryChange); // 浏览器前进/后退

// 统一的事件处理函数
function handleHistoryChange(event) {
  // 可以从 event.detail (自定义事件) 或 event.state (popstate事件) 中获取状态
  const state = event.detail ? event.detail.state : event.state;
  const url = event.detail ? event.detail.url : window.location.pathname;

  console.log('History changed. New state:', state, 'New URL:', url);
  // 这里根据 state 或 url 更新你的应用视图
  updateView(url);
}

// 示例更新视图函数
function updateView(url) {
  // 根据 url 渲染不同的组件或内容
  console.log('Rendering view for:', url);
}

// 现在使用 window.history.pushState 进行导航会触发 onstatechange 事件
window.history.pushState({ page: 1 }, '', '/home'); // 导航到 /home