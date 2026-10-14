#!/bin/zsh
set -euo pipefail

script_dir=${0:A:h}
staging_dir=$(mktemp -d /tmp/wanxiang-workflow.XXXXXX)
trap 'rm -rf "$staging_dir"' EXIT

mkdir -p "$staging_dir/src"
cp "$script_dir/info.plist" "$staging_dir/info.plist"
cp "$script_dir/icon.png" "$staging_dir/icon.png"
cp "$script_dir/README.md" "$staging_dir/README.md"
cp "$script_dir"/src/*.py "$staging_dir/src/"

rm -rf "$script_dir/wanxiang-updater.alfredworkflow"
(cd "$staging_dir" && zip -qr "$script_dir/wanxiang-updater.alfredworkflow" . -x '*/cache/*' '*/__pycache__/*' '*/.DS_Store' '*.json')
