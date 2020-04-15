#! /bin/bash

rm -r build || true

mkdir -p build/var/www/
pushd train-control
ng build
mv dist/train-control ../build/var/www/trains
popd
cp -r DEBIAN build/
mkdir -p build/etc/systemd/system
mkdir -p build/etc/nginx/sites-enabled

cp config/trains.conf build/etc/nginx/sites-enabled/trains.conf
cp config/trains.service build/etc/systemd/system/trains.service

#skip build anything non-python
mkdir -p build/usr/share/trains/trains
cp -r train-control-server/*.py build/usr/share/trains/
cp -r train-control-server/trains/*.py build/usr/share/trains/trains/


mkdir out || true

VERSION="$(git describe)"

sed -i "s/VERSIONHERE/${VERSION}/g" build/DEBIAN/control

fakeroot dpkg-deb -b build out