import argparse
import requests
import sys
import os


def get_headers():
    """读取 GitHub token 作为请求头。

    优先级: 环境变量 GH_TOKEN / GITHUB_TOKEN, 其次 ~/.gh_token 文件(供 cron/startup 这类无环境变量的场景)。
    为什么: 未认证 GitHub API 限流 60 次/小时/IP, VPS 上 cron 与 @reboot 脚本多次调用易触发 403 断链;
    带 token 提升到 5000 次/小时。token 存独立文件(600)而非写死在脚本里, 避免把密钥提交进 git 仓库。
    """
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return {"Authorization": f"Bearer {token}"}
    try:
        with open(os.path.expanduser("~/.gh_token")) as f:
            token = f.read().strip()
    except OSError:
        return {}
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def get_latest_valid_release(repo):
    """Fetch releases and find the latest one not starting with v0.0.0"""
    api_url = f"https://api.github.com/repos/{repo}/releases"
    try:
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        releases = response.json()

        # GitHub returns releases sorted by date (newest first)
        for release in releases:
            tag = release.get("tag_name", "")
            if not tag.startswith("v0.0.0"):
                return release
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching releases: {e}")
        sys.exit(1)


def _remove_quiet(path):
    """删临时文件, 失败不抛(清理路径不该覆盖真实错误)。"""
    try:
        os.remove(path)
    except OSError:
        pass


def download_file(url, dest_path):
    """Download a file from a URL to a local path.

    原子换入: 先写 <dest>.tmp, 再 os.replace 覆盖目标。
    为什么: 目标是正在运行的二进制时, 直接 open(dest, 'wb') 会得到
    Errno 26 Text file busy 而导致下载失败; 先写临时文件再 replace 可以
    热替换 —— 运行中的进程继续持有旧 inode 不受影响, 下次启动读新文件。
    """
    tmp_path = f"{dest_path}.tmp"
    try:
        print(f"Downloading from: {url}")
        with requests.get(url, stream=True, headers=get_headers()) as r:
            r.raise_for_status()
            with open(tmp_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        # 保留目标原有权限位(新文件默认 0644); 无旧文件时给 0755
        try:
            mode = os.stat(dest_path).st_mode & 0o777
        except OSError:
            mode = 0o755
        os.chmod(tmp_path, mode)
        os.replace(tmp_path, dest_path)
        print(f"Successfully saved to: {dest_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        _remove_quiet(tmp_path)
        sys.exit(1)
    except OSError as e:
        print(f"Error writing file: {e}")
        _remove_quiet(tmp_path)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Download a specific binary asset from the latest GitHub release.")
    
    # Flags
    parser.add_argument("--repo", required=True, help="Repo in 'owner/repo' format (e.g. helm/helm)")
    parser.add_argument("--dest", required=True, help="Local destination filename (e.g. my-app-linux)")
    parser.add_argument("--pattern", default="linux-amd64", help="Substring to match in the asset filename (default: linux-amd64)")

    args = parser.parse_args()

    print(f"Searching for latest release in {args.repo}...")
    release = get_latest_valid_release(args.repo)

    if not release:
        print("No release found that doesn't start with v0.0.0.")
        sys.exit(1)

    tag_name = release["tag_name"]
    print(f"Found valid release: {tag_name}")

    # Look for the specific asset (binary) in the release
    assets = release.get("assets", [])
    target_asset = None

    for asset in assets:
        if args.pattern.lower() in asset["name"].lower():
            target_asset = asset
            break

    if target_asset:
        print(f"Found matching asset: {target_asset['name']}")
        download_file(target_asset["browser_download_url"], args.dest)
    else:
        print(f"Could not find any asset containing '{args.pattern}' in release {tag_name}.")
        print("Available assets were:")
        for a in assets:
            print(f" - {a['name']}")
        sys.exit(1)

if __name__ == "__main__":
    main()