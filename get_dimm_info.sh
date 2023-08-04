#!/bin/bash
: "${1?Must provide node name}"
NODE_ID=$1
pwd=$(pwd)
ssh -o ConnectTimeout=5 -q $1 exit
echo $? > ssh_test.txt
echo $1 > node.txt
ssh -q -o ConnectTimeout=5 -o "StrictHostKeyChecking no" $1 dmidecode -t memory | grep -B6 Serial > dmidecode.txt
if python -c "import tabulate" &> /dev/null; then
    python $pwd/get_dimm_inventory_info.py
else
    pip install --proxy="http://proxy-us.intel.com:911" tabulate
    pip install --proxy="http://proxy-us.intel.com:911" xlrd
    python $pwd/get_dimm_inventory_info.py
fi