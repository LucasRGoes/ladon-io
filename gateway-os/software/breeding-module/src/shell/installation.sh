#!/bin/sh

#########################################
# Setup Ladon Gateway
#########################################

#########################################
# Variables
#########################################
newHostName="lgateway"
defaultUser="ladon"
defaultPassword="ladon"
rootPassword="ladon"
choice="y"
forceYesChoice="n"

#########################################
# Folders
#########################################
folderEtc="/etc/ladon"
folderFiles="/usr/share/ladon"
folderLog="/var/log/ladon"

#########################################
# Colors and Messages
#########################################
RED='\033[0;31m'
GREEN='\033[0;32m'
NORMAL='\033[0m' # No Color

error="${RED}ERROR:"
ok="${GREEN}OK!"
prefix="\\n${GREEN}[Ladon Gateway Installer]${NORMAL}"

#########################################
# Starting Script
#########################################
echo -e "$prefix Starting ..."

# Testing root privileges 
echo -e "$prefix Testing root privileges ..."
if [ "$EUID" -ne 0 ]; then 
  echo -e "$prefix $error Please run as root. Seeya!${NORMAL}"
  exit
else
  echo -e "$prefix $ok ${NORMAL}"
fi

echo -e "$prefix Updating hostname, motd, default user/passwd, root passwd ..."

read -e -p "Enter hostname (default: $newHostName) : " -i "$newHostName" newHostName
read -e -p "Enter user (default: $defaultUser) : " -i "$defaultUser" defaultUser
read -e -p "Enter new user default password (default: $defaultPassword) : " -i "$defaultPassword" defaultPassword
read -e -p "Enter root new password (default: $rootPassword) : " -i "$rootPassword" rootPassword

echo -e "$prefix Creating and setting up user '$defaultUser' ..."
id -u "$defaultUser" &> "/dev/null" || useradd "$defaultUser"
mkdir "/home/$defaultUser/" -p
chown "$defaultUser"  "/home/$defaultUser/" -R
echo -e "$defaultPassword\n$defaultPassword" | ( passwd "$defaultUser")
usermod -a -G sudo "$defaultUser"

# Root password
echo -e "$rootPassword\n$rootPassword" | ( passwd root)

# Setup hostname  
echo "$newHostName" > "/etc/hostname"

#########################################
# Initial Directives
#########################################

# Update, upgrade, dist-upgrade
echo -e "$prefix Updating, upgrading, dist-upgrading ..."
apt-get update && apt-get -y upgrade && apt-get -y dist-upgrade

echo -e "$prefix Creating folders ..."
mkdir -p $folderEtc
mkdir $folderEtc/pm2
mkdir -p $folderFiles
mkdir -p $folderLog
mkdir $folderLog/captures

#########################################
# Installing Basic Packages
#########################################
echo -e "$prefix Installing basic packages ..."

# Installing miscellaneous packages
apt-get install -y htop vim git curl

# Installing necessary packages
apt-get install -y mosquitto mosquitto-clients

echo -e "$prefix Updating time and locale ..."
locale-gen en_US en_US.UTF-8 pt_BR.UTF-8
dpkg-reconfigure locales
dpkg-reconfigure tzdata

#########################################
# Installing PM2
#########################################

# Installing Node.js
echo -e "$prefix Installing nodejs and npm ..."
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
apt-get install -y nodejs

# Installing PM2 and logrotate
echo -e "$prefix Installing pm2 and log rotate ..."
npm install pm2 -g
pm2 install pm2-logrotate

# Configuring logrotate
echo -e "$prefix Configuring log rotate ..."
pm2 set pm2-logrotate:max_size 50M
pm2 set pm2-logrotate:retain 1
pm2 set pm2-logrotate:dateFormat 'YYYY-MM-DD HH:mm Z'
pm2 set pm2-logrotate:workerInterval 60

pm2 unstartup
pm2 stop all
pm2 delete all

#########################################
# Installing OpenCV
#########################################

# Dependencies #
echo -e "$prefix Installing opencv dependencies ..."

# Developer Tools
apt-get install -y build-essential cmake pkg-config

# Image I/O Packages
apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

# Video I/O Packages
apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
apt-get install -y libxvidcore-dev libx264-dev

# GTK Development Library
apt-get install -y libgtk2.0-dev libgtk-3-dev

# Packages For Optimization
apt-get install -y libatlas-base-dev gfortran

# Installing Python3 Packages
apt-get install -y python3 python3-setuptools python3-dev

# Installing pip and numpy
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip3 install numpy

# Cleaning #
echo -e "$prefix Cleaning before building ..."
apt-get -y clean && apt-get -y autoclean && apt-get -y autoremove

# OpenCV Source Code #
mkdir opencv-build
cd opencv-build

# OpenCV Repository
git clone https://github.com/opencv/opencv.git

# OpenCV Contrib Repository
git clone https://github.com/opencv/opencv_contrib.git

# Cmake and its Options #
echo -e "$prefix Building opencv ..."
cd opencv
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
	-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
	-D WITH_CUDA=OFF \
	-D BUILD_TESTS=OFF \
	-D BUILD_PERF_TESTS= OFF ..

# Altering swap size at /etc/dphys-swapfile (1024)
cp ../../../files/etc/dphys-swapfile-opencv /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start

# Compiling with all four cores and installing OpenCV #
make -j4
make install

# Renaming OpenCV library
mv /usr/local/lib/python3.5/dist-packages/cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so

# Returning to old swap size at /etc/dphys-swapfile (100)
cp ../../../files/etc/dphys-swapfile-default /etc/dphys-swapfile
/etc/init.d/dphys-swapfile stop
/etc/init.d/dphys-swapfile start

# Cleaning directories and files
echo -e "$prefix Cleaning opencv ..."
cd ../../..
rm -r opencv-build

#########################################
# Starting Modules
#########################################

echo -e "$prefix Copying modules ..."
cp -r ../../../brain-module $folderFiles
cp -r ../../../tongue-module $folderFiles
cp files/etc/ladon/pm2/instances-ladon.json $folderEtc/pm2

echo -e "$prefix Starting modules ..."
pm2 start $folderEtc/pm2/instances-ladon.json

pm2 save
pm2 startup systemd

echo -e "$prefix Restarting ..."
shutdown -r 0
