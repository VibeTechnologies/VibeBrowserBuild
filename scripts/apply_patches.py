
import os
import subprocess

CHROMIUM_REPO = "https://chromium.googlesource.com/chromium/src.git"
CHROMIUM_DIR = "chromium_src"
PATCHES_DIR = "patches"

def clone_chromium():
    if not os.path.exists(CHROMIUM_DIR):
        print(f"Fetching Chromium repository into {CHROMIUM_DIR}...")
        subprocess.run(["fetch", "--no-history", "chromium"], check=True)
        print("Chromium fetched successfully.")
        print("Running gclient sync...")
        subprocess.run(["gclient", "sync"], cwd=CHROMIUM_DIR, check=True)
        print("gclient sync completed.")
    else:
        print(f"Chromium directory {CHROMIUM_DIR} already exists. Skipping fetch.")
        print("Running gclient sync to ensure all dependencies are up to date...")
        subprocess.run(["gclient", "sync"], cwd=CHROMIUM_DIR, check=True)
        print("gclient sync completed.")

def apply_patches():
    print("Applying patches...")
    patches_applied = False
    for patch_file in os.listdir(PATCHES_DIR):
        if patch_file.endswith(".patch"):
            patch_path = os.path.join(PATCHES_DIR, patch_file)
            print(f"Applying {patch_file}...")
            try:
                subprocess.run(["git", "-C", CHROMIUM_DIR, "apply", "--whitespace=fix", patch_path], check=True)
                print(f"Successfully applied {patch_file}.")
                patches_applied = True
            except subprocess.CalledProcessError as e:
                print(f"Error applying {patch_file}: {e}")
                print("Attempting to revert any partial changes...")
                subprocess.run(["git", "-C", CHROMIUM_DIR, "reset", "--hard"], check=True)
                print("Reverted to previous state.")
                exit(1)
    if not patches_applied:
        print("No patch files found in the 'patches' directory.")
    else:
        print("All patches applied successfully.")

if __name__ == "__main__":
    clone_chromium()
    apply_patches()
