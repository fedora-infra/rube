#!/bin/bash -e

./setup.sh

echo "running all tests"
for package in rube.{core,fedora}; do
    echo "[$package] running tests"
    pushd $package
    $(which nosetests)
    popd
    echo "[$package] done with tests"
done
