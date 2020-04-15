#! /bin/bash

rm -r out || true

mkdir -p out/var/www/
pushd train-control
ng build
mv dist/train-control ../out/var/www/trains
popd
cp -r DEBIAN out/
mkdir -p out/etc/systemd/system
mkdir -p out/etc/nginx/sites-enabled

cp config/trains.conf out/etc/nginx/sites-enabled/trains.conf
cp config/trains.service out/etc/systemd/system/trains.service

#skip out anything non-python
mkdir -p out/usr/share/trains/trains
cp -r train-control-server/*.py out/usr/share/trains/
cp -r train-control-server/trains/*.py out/usr/share/trains/trains/


mkdir build || true

VERSION="$(git describe)"

sed -i 's/VERSION/${VERSION}/g' out/DEBIAN/control

fakeroot dpkg-deb -b out build