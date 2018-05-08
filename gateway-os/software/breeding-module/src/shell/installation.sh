#!/bin/sh

# Before installation:
# - sudo raspi-config -> Update
# - sudo raspi-config -> Expand filesystem
# - sudo rpi-update
# - sudo shutdown -r 0 && exit

# Update, upgrade, dist-upgrade
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

# Installing miscellaneous packages
sudo apt-get install -y vim git

# Installing necessary packages
sudo apt-get install -y mosquitto mosquitto-clients

#########################################
# Installing PM2
#########################################

# Installing Node.js
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

# Installing PM2 and logrotate
sudo npm install pm2 -g
pm2 install pm2-logrotate

# Configuring logrotate

#########################################
# Installing OpenCV
#########################################

# Dependencies #

# Developer Tools
sudo apt-get install -y build-essential cmake pkg-config

# Image I/O Packages
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

# Video I/O Packages
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev

# GTK Development Library
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev

# Packages For Optimization
sudo apt-get install -y libatlas-base-dev gfortran

# Installing Python3 Packages
sudo apt-get install -y python3 python3-setuptools python3-dev

# Installing pip and numpy
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo pip3 install numpy

# Cleaning #
sudo apt-get -y clean && sudo apt-get -y autoclean && sudo apt-get -y autoremove

# OpenCV Source Code #

# OpenCV Repository
cd ~
git clone https://github.com/opencv/opencv.git

# OpenCV Contrib Repository
git clone https://github.com/opencv/opencv_contrib.git

# Cmake and its Options #
cd ~/opencv/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D BUILD_opencv_java=OFF \
	-D BUILD_opencv_python2=OFF \
	-D BUILD_opencv_python3=ON \
	-D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D BUILD_EXAMPLES=ON\
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D WITH_CUDA=OFF \
	-D BUILD_TESTS=OFF \
	-D BUILD_PERF_TESTS= OFF ..

# Altering swap size at /etc/dphys-swapfile (1024)
# sudo /etc/init.d/dphys-swapfile stop
# sudo /etc/init.d/dphys-swapfile start

# Compiling with all four cores and installing OpenCV #
make -j4
sudo make install

# Renaming OpenCV library
cd /usr/local/lib/python3.5/dist-packages/
sudo mv /usr/local/lib/python3.5/dist-packages/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

# Returning to old swap size at /etc/dphys-swapfile (100)
# sudo /etc/init.d/dphys-swapfile stop
# sudo /etc/init.d/dphys-swapfile start

# Cleaning directories and files
cd ~
sudo rm -r ./opencv
sudo rm -r ./opencv_contrib