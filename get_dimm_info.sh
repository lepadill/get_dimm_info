#!/bin/bash
: "${1?Must provide node name}"
NODE_ID=$1
ssh $1 dmidecode -t memory | grep -B6 Serial > dmidecode.txt
pwd=$(pwd)
python $pwd/get_dimm_inventory_info.py
echo

