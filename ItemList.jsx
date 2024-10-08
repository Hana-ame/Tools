import React, { useState } from 'react';

function ItemList() {
  const [items, setItems] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleAddItem = () => {
    if (inputValue.trim() !== '') {
      setItems([...items, inputValue]);
      setInputValue(''); // 清空输入框
    }
  };

  const handleRemoveItem = (index) => {
    const newItems = items.filter((_, i) => i !== index);
    setItems(newItems);
  };

  return (
    <div className="p-5">
      <h1 className="text-2xl font-bold mb-4">Item List</h1>

      <div className="flex mb-4">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Add a new item"
          className="border border-gray-300 rounded-l-md p-2 flex-grow"
        />
        <button
          onClick={handleAddItem}
          className="bg-blue-500 text-white rounded-r-md px-4 hover:bg-blue-600"
        >
          Add Item
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {items.map((item, index) => (
          <div
            key={index}
            className="relative border border-gray-300 rounded-lg p-4 shadow-md"
          >
            <button
              onClick={() => handleRemoveItem(index)}
              className="absolute top-2 right-2 text-red-500 hover:text-red-700"
            >
              &times; {/* 使用 × 符号作为删除按钮 */}
            </button>
            <p className="text-lg">{item}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ItemList;