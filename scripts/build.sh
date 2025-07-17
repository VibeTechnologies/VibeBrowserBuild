#!/bin/sh
set -eu
gn gen out/Debug --args='is_debug=true symbol_level=2'
exec ninja -C out/Debug chrome

