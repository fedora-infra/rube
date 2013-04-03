#!/bin/bash -e

echo "Installing all packages in development mode"
for package in rube.{core,fedora}; do
    echo "[$package] Installing"
    pushd $package
    python setup.py develop
    popd
    echo "[$package] done."
done
