# Tools Collection

A comprehensive collection of software engineering tools, automation scripts, and utility helpers.

## 📂 Project Structure & Tool Directory

### 🖼️ Image Processing
Tools for format conversion and metadata cleaning.
- `!clear PNG info(drag files in).py`: Clears PNG metadata.
- `!make jpg file(drag files in).py`: Batch converts images to JPG.
- `!pic2webp.py`: Converts images to WebP.
- `!webp2jpg.py`: Converts WebP to JPG.
- `conv2avif.py` / `convert_to_avif.py`: Converts images to AVIF format.
- `gif2webp.py`: Converts GIFs to WebP.
- `x连发图.py`: Specialized image processing tool.
- `archive/ConvertToMono.py`: Converts images to monochrome.

### 📄 File & Data Manipulation
Utilities for file backup, encoding, and renaming.
- `!drag_files_in.py`: Generic wrapper for processing dragged files.
- `!rename(drag folder in).py`: Batch renames files in a folder (Windows focused).
- `append_byte.py`: Appends bytes to files.
- `bak_files.py`: File backup utility.
- `convert_base64.py` / `extract_base64.py`: Base64 encoding/decoding.
- `archive/!Shift-JIS 2 UTF-8...`: Encoding converters (Shift-JIS, UTF-8, UCS-2).
- `archive/utils.py`: File hashing (SHA-256) and other helpers.

### 🌐 Network & Proxy
Scripts for network tunneling, proxies, and connectivity.
- `proxy.sh` / `proxy_rtmp.sh`: Proxy setup scripts.
- `local_proxy.sh` / `remote_proxy.sh`: Local and remote proxy management.
- `nc_proxy.sh` / `nc_rtmp.sh`: Netcat-based proxying.
- `set_proxy.source`: Proxy environment configuration.
- `scripts/ssh.sh` / `scripts/scp.sh`: SSH and SCP wrappers.
- `scripts/remote_proxy.sh`: Remote proxy automation.

### 🤖 Web & Automation
Scrapers, uploaders, and web-based tool interfaces.
- `download_twitter.py`: Twitter resource downloader.
- `download_edgedriver_win64.py`: Automates EdgeDriver download.
- `file_uploader.py` / `file_post_tool.py`: File upload utilities.
- `exhentai_BBcode.py`: BBCode generator for ExHentai.
- `wnacg.py`: Specialized web tool.
- `obs.py`: OBS related automation.
- `archive/excurl.py`: Curl wrapper for specific web requests.
- `archive/moonchan-poster.py`: Automated posting to Moonchan.
- `archive/save_ero_imgs.py`: Image scraping tool.

### ⚙️ System Core & Framework
The backbone of the toolset, including runners and listeners.
- `agent_runner.py`: Core execution framework for agents.
- `command_listener.py`: Listens for and executes system commands.
- `funcs.py` / `my_tools.py` / `my_file.py` / `my_time.py`: General purpose internal libraries.
- `wake.py` / `stdin.py`: System interaction utilities.
- `scripts/kill_process.sh`: Process termination utility.
- `scripts/remote.service`: Systemd service configuration.

### 📊 Data, Math & Reports
Mathematical calculations and report generation.
- `calculation.py` / `sine.py`: Mathematical utility functions.
- `generate_html.py` / `generate_json.py`: Report generators.
- `MedianAverageTracker.py`: Data tracking and averaging tool.
- `misc/normal.py`: Normal distribution calculations.

### 🛠️ Other Modules
- **Tampermonkey**: Browser userscripts in `tampermonkey/` (Bilibili, YouTube, etc.).
- **Websocket**: Server and DAO implementations in `websocket/`.
- **OpenRoute**: LLM API wrappers in `openroute/`.
- **Neko**: Specialized scripts in `neko/`.

## 🚀 Usage
Most scripts in the root directory can be run directly via Python:
\`\`\`bash
python <script_name>.py
\`\`\`
Scripts starting with `!` are designed to be used by dragging and dropping files onto the script icon (on Windows).
