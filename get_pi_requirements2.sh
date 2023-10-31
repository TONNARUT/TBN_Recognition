#!/bin/bash

# Get packages required for OpenCV

sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install qt4-dev-tools 
sudo apt-get -y install libatlas-base-dev


# Need to get an older version of OpenCV because version 4 has errors
pip3 install opencv-python==4.6.0.66

#========================================================================================= 
#pip3 install tensorflow 2.9.1
#if successfully installed, the following modules are installed:
#   absl-py-1.4.0 astunparse-1.6.3 cachetools-5.3.1 flatbuffers-1.12 
#   gast-0.4.0 google-auth-2.22.0 google-auth-oauthlib-0.4.6 google-pasta-0.2.0 grpcio-1.57.0 
#   h5py-3.9.0 keras-2.9.0 keras-preprocessing-1.1.2 libclang-16.0.6 opt-einsum-3.3.0 packaging-23.1 
#   protobuf-3.19.6 pyasn1-0.5.0 pyasn1-modules-0.3.0 rsa-4.9 tensorboard-2.9.1 
#   tensorboard-data-server-0.6.1 tensorboard-plugin-wit-1.8.1 tensorflow-2.9.1 
#   tensorflow-estimator-2.9.0 tensorflow-io-gcs-filesystem-0.33.0 termcolor-2.3.
#========================================================================================= 
# install gdown to download from Google drive
sudo -H pip3 install gdown
# download the wheel
gdown https://drive.google.com/uc?id=1xP6ErBK85SMFnQamUh4ro3jRmdCV_qDU
# install TensorFlow 2.9.1
sudo -H pip3 install tensorflow-2.9.1-cp39-cp39-linux_aarch64.whl
#========================================================================================= 

#sudo pip3 install pillow
sudo pip3 install pyttsx3==2.90
sudo pip3 install pillow==9.1.0 
sudo pip3 install numpy==1.23.1
sudo pip3 install datetime



