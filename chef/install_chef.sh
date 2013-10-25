#! /bin/bash
#License: GPLv3

sudo apt-get update
sudo apt-get install git
sudo apt-get install curl
curl -L https://www.opscode.com/chef/install.sh | sudo bash

# downloads community cookbooks
cd $HOME/chef-solo/cookbooks

git clone https://github.com/opscode-cookbooks/git.git
git clone https://github.com/opscode-cookbooks/build-essential.git
git clone https://github.com/opscode-cookbooks/dmg.git
git clone https://github.com/opscode-cookbooks/runit.git
git clone https://github.com/opscode-cookbooks/yum.git
git clone https://github.com/opscode-cookbooks/windows.git
git clone https://github.com/opscode-cookbooks/chef_handler.git
git clone https://github.com/opscode-cookbooks/openssl.git
git clone https://github.com/opscode-cookbooks/apt.git

git clone https://github.com/opscode-cookbooks/database.git
git clone https://github.com/opscode-cookbooks/mysql.git
git clone https://github.com/opscode-cookbooks/xfs.git
git clone https://github.com/opscode-cookbooks/aws.git

git clone https://github.com/opscode-cookbooks/application.git
git clone https://github.com/opscode-cookbooks/application_python.git
git clone https://github.com/opscode-cookbooks/python.git
git clone https://github.com/opscode-cookbooks/gunicorn.git
git clone https://github.com/opscode-cookbooks/supervisor.git
git clone https://github.com/opscode-cookbooks/postgresql.git



