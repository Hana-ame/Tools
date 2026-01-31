# 需要重新npm run start

sed -i "/      alias: {/c \      alias: {\n        '@': path.resolve('src')," node_modules/react-scripts/config/webpack.config.js