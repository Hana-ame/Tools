import argparse
import requests
import sys
import os

def get_latest_valid_release(repo):
    """Fetch releases and find the latest one not starting with v0.0.0"""
    api_url = f"https://api.github.com/repos/{repo}/releases"
    try:
        response = requests.get(api_url)
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

def download_file(url, dest_path):
    """Download a file from a URL to a local path"""
    try:
        print(f"Downloading from: {url}")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Successfully saved to: {dest_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
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
