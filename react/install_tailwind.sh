# https://claude.ai/chat/f19ff3fd-79f5-483a-a2eb-2a44f40e6e72

# 安装Tailwind和其他必要的依赖
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

# 生成Tailwind配置文件
npx tailwindcss init -p

# 在src目录下创建index.css文件（如果还没有的话）
touch src/index.css

# 在src/index.css文件中添加Tailwind指令
echo "@tailwind base;
@tailwind components;
@tailwind utilities;" > src/index.css

# 修改tailwind.config.js文件
echo "module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}" > tailwind.config.js

# 确保在src/index.js中导入了CSS文件
sed -i "1i import './index.css';" src/index.js

# 重新启动开发服务器
npm start