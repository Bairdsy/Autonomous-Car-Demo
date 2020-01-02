#!/bin/bash

#set -x

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
BASEDIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

#Python
#conda activate

# GPU
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export PATH=/usr/local/cuda/bin:$PATH

# App
export APP=/app
export SASHOME=/opt/sas/viya
export DFESP_HOME=$SASHOME/home/SASEventStreamProcessingEngine/6.1
export SASTK=$SASHOME/home/SASFoundation/sasexe

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DFESP_HOME/lib:${SASTK}:$DFESP_HOME/ssl/lib
export TKPATH=$DFESP_HOME/lib/tk.940m3

export DFESP_SA_YAML=$DFESP_HOME/etc/sa_windows/sa_windows.yml
export PATH=$PATH:$DFESP_HOME/bin
export DFESP_SSLPATH=$DFESP_HOME/ssl/lib
export DFESP_JAVA_TRUSTSTORE=$SASHOME/config/etc/SASSecurityCertificateFramework/cacerts/trustedcerts.jks
export SSLCALISTLOC=$SASHOME/config/etc/SASSecurityCertificateFramework/cacerts/trustedcerts.pem

#git clone https://github.com/sassoftware/python-esppy.git
export PYTHONPATH="$SASHOME/home/SASEventStreamProcessingEngine/current/lib/:$APP/python-esppy"

OBJDET="$BASEDIR/server.py"
exec python $OBJDET $@
