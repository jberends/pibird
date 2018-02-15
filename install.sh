#!/usr/bin/env bash
# ensure installation of the proper software on the rpi

# locales fix
sudo locale-gen en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
dpkg-reconfigure locales

# Pimoroni speakerhat
curl -sS https://get.pimoroni.com/speakerphat | bash

# nessary libraries
sudo apt install mpg321

# automatic testing
~/Pimoroni/speakerphat/test/test.sh


# additional stuff
sudo apt install libav-tools libavcodec-extra ffmpeg