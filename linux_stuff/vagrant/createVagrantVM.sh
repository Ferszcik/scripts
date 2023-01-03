#!/bin/bash

# vagrant halt - stop vm aka shutdown
# vagrant destroy - kill instance of vm but don't remove vagrant resources
# vagrant box remove - remove all vagrant resources, this will require vagrant to download it again when creating new vm

# Define colors for echo printing
NC='\033[0m'
RED='\033[0;31m'

# Check if argument is present
if [[ "${1}" = "" ]]
then
	echo -e "${RED}ERROR:${NC} Please provide CentOS version you want to create"
	exit
fi

# Create directory for Vagrant VM and init Vagrantfile
if [[ ! -d "vagrantBoxCentos${1}" ]]
then
	mkdir ~/vagrantBoxCentos${1}
fi

cd ~/vagrantBoxCentos${1}/
vagrant init generic/centos${1}

# Remove default Vagrantfile and replace with custom one
rm Vagrantfile
cd - > /dev/null 2>&1

cp $PWD/myVagrantfile ~/vagrantBoxCentos${1}/Vagrantfile
cp $PWD/startupScript.sh ~/vagrantBoxCentos${1}/startupScript.sh

cd - > /dev/null 2>&1
sed -i 's/centos[0-9]/centos'${1}'/g' Vagrantfile

# Start Vagrant VM and connect via SSH
vagrant up
vagrant ssh centos${1}
