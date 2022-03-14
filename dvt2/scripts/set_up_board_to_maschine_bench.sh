#!/bin/bash

GIT_USER=samuel.pelegrinello

cd ~

git clone --depth=1 https://${GIT_USER}@bitbucket.bln.native-instruments.de/scm/mas/maschine-test-data.git
git clone --depth=1 https://${GIT_USER}@bitbucket.bln.native-instruments.de/scm/mas/maschine.git

cp -r maschine-test-data/Headless/Projects/ maschine/robot-tests/Tests-Headless/
rm -r maschine-test-data/Headless/Projects/

sh /home/root/maschine/robot-tests/Tests-Headless/scripts/install_python_dependecies_run_once.sh

git clone --depth=1 https://${GIT_USER}@bitbucket.bln.native-instruments.de/scm/testau/robot-framework-libs.git

cd robot-framework-libs
python setup.py install
cd ..

git clone --depth=1 https://samuel.pelegrinello@bitbucket.bln.native-instruments.de/scm/emb/rtirq.git

