#!/bin/bash

set -e
set +x

SCRIPT_DIR="$(realpath ${BASH_SOURCE[0]})"

pushd "$SCRIPT_DIR"

rm -rf ./build_debug
rm -rf ./build_release
rm -rf ./cmake/output

popd
