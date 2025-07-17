# Chromium Fork Patch Management

This repository contains a Python script to manage a Chromium fork by cloning the official Chromium source and applying custom patches.

## Files:

*   `apply_patches.py`: A Python script to clone the Chromium repository and apply patches.
*   `patches/`: This directory contains `.patch` files that will be applied to the Chromium source.

## Usage:

1.  **Clone this repository:**
    ```bash
    git clone <your-new-github-repo-url>
    cd <your-new-github-repo-name>
    ```

2.  **Install depot_tools:**
    Run the provided script to install `depot_tools` and add it to your PATH. You might need to restart your terminal or `source` your shell's RC file (`.bashrc` or `.zshrc`) after running this.
    ```bash
    ./install_depot_tools.sh
    ```

3.  **Run the patch application script:**
    ```bash
    python apply_patches.py
    ```
    This script will:
    *   Use `fetch --no-history chromium` to get the Chromium source code into a `chromium_src` directory if it doesn't already exist.
    *   Run `gclient sync` to ensure all dependencies are downloaded.
    *   Apply all `.patch` files found in the `patches/` directory to the `chromium_src` directory.

## Generating New Patches:

To generate new patches from your Chromium fork, navigate to your Chromium source directory (`chromium_src`) and use `git diff`. For example, to create a patch from your current changes against the `main` branch:

```bash
cd chromium_src
git diff main > ../patches/my_new_feature.patch
```

Then, move the generated patch file into the `patches/` directory of this repository.

## Setting up a New GitHub Repository:

1.  **Create a new empty repository on GitHub.** Do NOT initialize it with a README or license.
2.  **Initialize a Git repository in this directory:**
    ```bash
    git init
    ```
3.  **Add your files:**
    ```bash
    git add .
    ```
4.  **Commit your changes:**
    ```bash
    git commit -m "Initial commit: Chromium fork patch management system"
    ```
5.  **Add the remote origin (replace with your GitHub repository URL):**
    ```bash
    git remote add origin <your-new-github-repo-url>
    ```
6.  **Push your changes to GitHub:**
    ```bash
    git push -u origin master
    ```