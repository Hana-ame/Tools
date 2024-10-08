// not work for 5.0.1

import React from 'react';
import ReactMarkdown from 'react-markdown';
// import 'tailwindcss/base';
// import 'tailwindcss/components';
// import 'tailwindcss/utilities';

const MarkdownViewer = ({ markdownText }) => {
  const renderers = {
    heading: ({ level, children }) => (
      <h1 className={`text-${level}xl font-bold mb-4`}>{children}</h1>
    ),
    paragraph: ({ children }) => (
      <p className="text-lg leading-relaxed mb-4">{children}</p>
    ),
    link: ({ href, children }) => {
      if (href.startsWith('https://example.com/')) {
        return (
          <div className="bg-white shadow-md p-4 mb-4">
            <h2 className="text-lg font-bold mb-2">{children}</h2>
            <p className="text-gray-600">{getSummary(href)}</p>
          </div>
        );
      }
      return <a href={href}>{children}</a>;
    },
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <ReactMarkdown source={markdownText} renderers={renderers} />
    </div>
  );
};

const getSummary = (href) => {
  // 自定义逻辑来获取摘要内容
  // 例如：发送请求到服务器获取摘要内容
  return '这是一个摘要内容';
};

export default MarkdownViewer;