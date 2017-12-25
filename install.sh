#!/bin/bash

cp undervolt.py /usr/bin/undervolt
cp config.json /etc/undervolt.json
cp undervolt.service /etc/systemd/system/
systemctl enable undervolt
systemctl restart undervolt