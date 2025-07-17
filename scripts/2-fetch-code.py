#!/usr/bin/env python3
import os
import subprocess
import sys

CHROMIUM_REPO = "https://chromium.googlesource.com/chromium/src.git"
import os
import subprocess
import sys

CHROMIUM_DIR = "src"  # Changed from chromium_src to src, which is what fetch chromium creates
PATCHES_DIR = "patches"

script_dir = os.path.abspath(os.path.dirname(__file__))
chromium_dir_path = os.path.join(script_dir, CHROMIUM_DIR)
patches_dir_path = os.path.join(script_dir, "..", PATCHES_DIR)


def is_inside_chromium_checkout(script_path):
    """
    Walk up from script_path, looking for .gclient or src/.git to determine if we're inside a Chromium checkout.
    """
    dir_path = os.path.abspath(os.path.dirname(script_path))
    while True:
        if os.path.exists(os.path.join(dir_path, ".gclient")):
            return True
        if os.path.exists(os.path.join(dir_path, "src", ".git")):
            return True
        parent = os.path.dirname(dir_path)
        if parent == dir_path:
            break
        dir_path = parent
    return False

def clone_chromium():
    # Check if we're already in a directory with .gclient file (indicates chromium workspace)
    gclient_path = os.path.join(script_dir, ".gclient")
    if os.path.exists(gclient_path):
        return
    elif os.path.exists(chromium_dir_path):
        print(f"Chromium directory {chromium_dir_path} exists but no .gclient file found.")
        print("This might be a standalone git clone. Checking if it's a valid Chromium repo...")
        if os.path.exists(os.path.join(chromium_dir_path, ".git")):
            try:
                # Check if this is actually a Chromium repository
                result = subprocess.run(["git", "-C", chromium_dir_path, "remote", "get-url", "origin"], 
                                      capture_output=True, text=True, check=True)
                if "chromium" in result.stdout.lower():
                    print("Valid Chromium repository found. Updating...")
                    subprocess.run(["git", "-C", chromium_dir_path, "pull"], check=True)
                    print("Repository updated.")
                else:
                    print("Directory exists but doesn't appear to be a Chromium repository.")
                    print("Please remove the directory or choose a different location.")
                    sys.exit(1)
            except subprocess.CalledProcessError:
                print("Could not determine repository origin. Assuming it's valid and continuing...")
        else:
            print(f"Directory {chromium_dir_path} exists but is not a git repository.")
            print("Please remove the directory or choose a different location.")
            sys.exit(1)
    else:
        # Check if 'fetch' is available in PATH
        from shutil import which
        if which('fetch') is None:
            print("Error: 'fetch' command not found in PATH. Please ensure depot_tools is installed and added to your PATH.")
            sys.exit(1)
        print(f"Fetching Chromium repository (with caffeinate)...")
        fetch_cmd = f"cd '{script_dir}' && caffeinate fetch --no-history chromium"
        result = subprocess.run(fetch_cmd, shell=True, check=True)


def apply_patches():
    print("Applying patches...")
    patches_applied = False
    
    # Check if patches directory exists
    if not os.path.exists(patches_dir_path):
        print(f"Patches directory '{patches_dir_path}' not found.")
        return
    
    # Get all patch files and sort them
    patch_files = [f for f in os.listdir(patches_dir_path) if f.endswith(".patch")]
    patch_files.sort()  # Apply patches in alphabetical order
    
    if not patch_files:
        print("No patch files found in the 'patches' directory.")
        return
    
    for patch_file in patch_files:
        patch_path = os.path.join(patches_dir_path, patch_file)
        print(f"Applying {patch_file}...")
        
        # First, check if the patch can be applied (dry run)
        try:
            subprocess.run(["git", "-C", CHROMIUM_DIR, "apply", "--check", patch_path], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print(f"Patch {patch_file} cannot be applied (may already be applied or conflicts exist).")
            print("Checking if patch is already applied...")
            
            # Try to apply in reverse to check if it's already applied
            try:
                subprocess.run(["git", "-C", CHROMIUM_DIR, "apply", "--check", "--reverse", patch_path], 
                             check=True, capture_output=True)
                print(f"Patch {patch_file} appears to be already applied. Skipping.")
                continue
            except subprocess.CalledProcessError:
                print(f"Patch {patch_file} has conflicts or cannot be applied.")
                print("You may need to resolve conflicts manually or reset the repository.")
                
                # Ask user what to do
                response = input("Do you want to continue with the next patch? (y/n): ")
                if response.lower() != 'y':
                    print("Patch application aborted.")
                    sys.exit(1)
                continue
        
        # Apply the patch
        try:
            subprocess.run(["git", "-C", CHROMIUM_DIR, "apply", "--whitespace=fix", patch_path], check=True)
            print(f"Successfully applied {patch_file}.")
            patches_applied = True
        except subprocess.CalledProcessError as e:
            print(f"Error applying {patch_file}: {e}")
            print("Attempting to revert any partial changes...")
            subprocess.run(["git", "-C", CHROMIUM_DIR, "reset", "--hard"], check=True)
            print("Reverted to previous state.")
            sys.exit(1)
    
    if patches_applied:
        print("All applicable patches applied successfully.")
    else:
        print("No new patches were applied (all patches may already be applied).")

if __name__ == "__main__":
    # Use the script's own path to determine if we're inside a Chromium checkout
    script_path = os.path.abspath(__file__)
    if is_inside_chromium_checkout(script_path):
        print("Script is running from inside a Chromium checkout. Skipping clone/fetch step.")
    else:
        clone_chromium()
    apply_patches()
