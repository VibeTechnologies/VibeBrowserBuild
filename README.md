# Chromium Patch Workflow

## 1. Install dependencies and depot_tools
```sh
scripts/1-install-tools.sh
source ~/.zshrc   # or source ~/.bashrc
```

## 2. Fetch Chromium and apply patches
```sh
scripts/2-fetch-code.py
```

## 3. Configure debug build
```sh
scripts/3-configure-debug.sh
```

## 4. Build Chromium (Debug)
```sh
scripts/4-build-debug.sh
```

## Notes
- Place your `.patch` files in the `patches/` directory before step 2.
- depot_tools will be installed in `~/depot_tools` and added to your shell PATH.
    git push -u origin master
    ```