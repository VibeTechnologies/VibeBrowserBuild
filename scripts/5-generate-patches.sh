#!/bin/bash

# Script to generate git patches from a specific commit
# Usage: ./generate_patches.sh [commit_hash]

set -e  # Exit on any error

# Default commit hash
DEFAULT_COMMIT="44d34f8db54149e05093fd34ee607db44e48fa26"
COMMIT_HASH="${1:-$DEFAULT_COMMIT}"
BUILD_REPO_PATH=$(readlink -f "$(dirname "$0")/../")
PATCHES_DIR="$BUILD_REPO_PATH/patches"

echo "Generating git patches from commit: $COMMIT_HASH"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Verify the commit exists
if ! git cat-file -e "$COMMIT_HASH" 2>/dev/null; then
    echo "Error: Commit $COMMIT_HASH does not exist"
    exit 1
fi

# Create patches directory if it doesn't exist
mkdir -p "$PATCHES_DIR"

# Clean existing patches
echo "Cleaning existing patches in $PATCHES_DIR/"
rm -f "$PATCHES_DIR"/*.patch

# Generate patches from the specified commit to HEAD
echo "Generating patches from $COMMIT_HASH to HEAD..."

# Get the number of commits from the specified commit to HEAD
COMMIT_COUNT=$(git rev-list --count "$COMMIT_HASH"..HEAD)

if [ "$COMMIT_COUNT" -eq 0 ]; then
    echo "No commits found between $COMMIT_HASH and HEAD"
    echo "Generating a single patch for the specified commit..."
    
    # Generate a patch for just the specified commit
    git format-patch -1 "$COMMIT_HASH" --output-directory="$PATCHES_DIR" --numbered
else
    echo "Found $COMMIT_COUNT commits to generate patches for"
    
    # Generate patches for all commits from the specified commit to HEAD
    git format-patch "$COMMIT_HASH" --output-directory="$PATCHES_DIR" --numbered
fi

# List generated patches
echo ""
echo "Generated patches in $PATCHES_DIR/:"
ls -la "$PATCHES_DIR"/*.patch 2>/dev/null || echo "No patches generated"
