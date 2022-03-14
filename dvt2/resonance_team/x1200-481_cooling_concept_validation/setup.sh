#!/bin/bash

mkdir -p /usr/etc/
cp cooling_validation.service /etc/systemd/system
cp x1200-481_cooling_concept_validation.sh /usr/etc/

systemctl enable cooling_validation.service