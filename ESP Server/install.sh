#!/bin/bash
set -x
# Download the Linux Anaconda Distribution
#Use curl
curl -o ~/anaconda3.sh https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
#wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh -O ~/anaconda3.sh

#remove
rm -rf $HOME/anaconda3
# Run the installer
bash ~/anaconda3.sh -b -p $HOME/anaconda3

### Run the conda init script to setup the shell
echo ". $HOME/anaconda3/etc/profile.d/conda.sh" >> $HOME/.bashrc
. $HOME/anaconda3/etc/profile.d/conda.sh


cd /app
#delete if exist
rm -rf python-esppy
git clone https://github.com/sassoftware/python-esppy.git

# Install necessary Python packages
conda env create --file espdeploy/conda/conda.yaml

#conda env create --file conda2.yaml
#conda env update --file iotdemo/conda/iotdemo.yaml
#conda activate iotdemo
echo "conda activate iotdemo" >> ~/.bashrc

echo "Installation completed - App files copied into /app"
