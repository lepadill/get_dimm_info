#!/bin/bash
: "${1?Must provide node name}"
NODE_ID=$1
pwd=$(pwd)
sed -i /$1/d ~/.ssh/known_hosts
ssh $1 dmidecode -t memory | grep -B6 Serial > dmidecode.txt
python $pwd/get_dimm_inventory_info.py


