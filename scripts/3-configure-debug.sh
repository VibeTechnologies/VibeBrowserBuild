#!/bin/bash
export PATH=$HOME/depot_tools:$PATH
exec gn gen out/Debug --args='is_debug=true symbol_level=2'