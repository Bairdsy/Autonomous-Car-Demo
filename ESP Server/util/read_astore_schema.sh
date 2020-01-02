#!/bin/bash

exec 2>/dev/null

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"


export DFESP_HOME=/opt/sas/viya/home/SASEventStreamProcessingEngine/6.1
export SASTK=/opt/sas/viya/home/SASFoundation/sasexe
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DFESP_HOME/lib:${SASTK}:$DFESP_HOME/ssl/lib
export TKPATH=$DFESP_HOME/lib/tk.940m3
export PATH=$PATH:$DFESP_HOME/bin

input_path="$(dirname ${1})"
input_file="$(basename ${1})"

pushd ${input_path} > /dev/null
dfesp_analytics -score -type astore -reference ${input_file}
popd > /dev/null
