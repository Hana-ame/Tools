// not work for 5.0.1

import { useState } from "react";
import MarkdownViewer from "./MarkdownViewer";

const MarkdownEditor = () => {
  const [markdownText, setMarkdownText] = useState('');
  const [previewText, setPreviewText] = useState('');

  const handleInputChange = (event) => {
    setMarkdownText(event.target.value);
    setPreviewText(event.target.value);
  };

  return (
    <div className="app-container">
      <div className="editor-container">
        <textarea
          className="editor-textarea"
          value={markdownText}
          onChange={handleInputChange}
        />
      </div>
      <div className="preview-container">
        <MarkdownViewer markdownText={previewText} />
      </div>
    </div>
  );
};
export default MarkdownEditor;