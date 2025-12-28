import sys
import os
import json
import shutil
import urllib.request
from pathlib import Path

PROJECT_ID = "dev-init-8fd3e"
COLLECTION = "projects"

# Per-tool progress bar
def progress_bar(block, block_size, total_size):
    percent = min(100, int((block * block_size / total_size) * 100))
    filled = int(percent / 2)
    bar = "█" * filled + "-" * (50 - filled)
    sys.stdout.write(f"\r|{bar}| {percent}%")
    sys.stdout.flush()

# Download and save to system Downloads folder
def download_file(url, filename, tool):
    download_dir = str(Path.home() / "Downloads")
    file_path = os.path.join(download_dir, filename)

    print(f"\nDownloading {tool} → saving to Downloads folder...")
    urllib.request.urlretrieve(url, file_path, reporthook=progress_bar)
    print(f"\n{tool} → {filename} saved to Downloads ✔\n")

# System-level tool detection for all tools
def tool_exists_system(tool):
    tool = tool.lower()

    # VS Code detection
    if tool == "vscode":
        paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
        ]
        return any(os.path.exists(p) for p in paths)

    # Notepad++
    if tool == "notepad++":
        return os.path.exists(r"C:\Program Files\Notepad++\notepad++.exe")

    # Git
    if tool == "git":
        return shutil.which("git") is not None

    # Any other CLI tool (node, python, javac, etc.)
    return shutil.which(tool) is not None

# Smart URL matcher for all tools
def find_matching_url(tool, url_list):
    tool = tool.lower()

    keywords = {
        "vscode": ["visualstudio", "vs code", "code.exe", "vscode"],
        "notepad++": ["notepad", "npp", "notepad++", "installer"],
        "git": ["git", "git-scm", "git-setup"]
    }

    for url in url_list:
        if any(k in url.lower() for k in keywords.get(tool, [tool])):
            return url

    return None

# This must exist for CLI entry point
def main():
    if len(sys.argv) < 2:
        print("Usage: dev_setup <project-name>")
        sys.exit(1)

    project_name = sys.argv[1].lower()

    # --- Fetch Firestore JSON from Firebase ---
    try:
        api_url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/{COLLECTION}"
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            docs = data.get("documents", [])
    except Exception as e:
        print("Failed to fetch Firebase data :", e)
        sys.exit(1)

    # --- Find your project data ---
    project_fields = None
    for doc in docs:
        fields = doc.get("fields", {})
        pname = fields.get("projectName", {}).get("stringValue", "").lower()
        if pname == project_name:
            project_fields = fields
            break

    if not project_fields:
        print("Project not found ")
        sys.exit(1)

    # --- Convert Firestore response to normal dict ---
    config = {k: list(v.values())[0] for k, v in project_fields.items()}
    print("\nProject Config Pulled:\n", json.dumps(config, indent=2))

    # --- Split URLs stored as one string ---
    url_list = [u.strip() for u in config.get("sourceUrls", "").split(",")]

    # --- Split tools list fetched from Firebase ---
    tools = [t.strip().lower() for t in config.get("tools", "").split(",")]

    print("\nChecking installed tools & downloading missing ones...\n")

    for tool in tools:
        print(f"Checking: {tool}")

        if tool_exists_system(tool):
            print(f"{tool} already installed on system, skipping \n")
            continue

        matched_url = find_matching_url(tool, url_list)

        if not matched_url:
            print(f"{tool} → No valid URL found \n")
            continue

        filename = matched_url.split("?")[0].split("/")[-1]
        if not filename:
            filename = tool + "_setup.exe"

        download_file(matched_url, filename, tool)

    print("All tools processed Setup complete!")

if _name_ == "_main_":
    main()
