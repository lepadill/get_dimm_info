#!/bin/bash
#Parameters
: "${1?Must provide node name}"
NODE_ID=$1
ssh $1 dmidecode -t memory | grep -A 1 Serial > dmidecode.txt
pwd=$(pwd)
python $pwd/get_dimm_inventory_info.py
