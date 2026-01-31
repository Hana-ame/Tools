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
    """Download a file from a URL to a local path using streaming"""
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
    parser = argparse.ArgumentParser(description="Download the latest GitHub release (excluding v0.0.0).")
    
    # Define flags
    parser.add_argument("--repo", required=True, help="GitHub repository in 'owner/repo' format (e.g., google/googletest)")
    parser.add_argument("--dest", required=True, help="Destination filename (e.g., release.zip)")

    args = parser.parse_args()

    print(f"Searching for latest release in {args.repo}...")
    release = get_latest_valid_release(args.repo)

    if not release:
        print("No release found that doesn't start with v0.0.0.")
        sys.exit(1)

    tag_name = release["tag_name"]
    # We download the 'zipball_url' which is the source code for that release
    download_url = release["zipball_url"]

    print(f"Found valid release: {tag_name}")
    download_file(download_url, args.dest)

if __name__ == "__main__":
    main()