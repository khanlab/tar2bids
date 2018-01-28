Bootstrap: shub
From: khanlab/heudiconv:0.4.3

%setup
mkdir -p $SINGULARITY_ROOTFS/opt/tar2bids
cp -Rv . $SINGULARITY_ROOTFS/opt/tar2bids

%post 
mkdir -p /src

## Install bids-validator
apt-get update && \
apt-get install -y curl git && \
curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
apt-get remove -y curl && \
apt-get install -y nodejs && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

git clone http://github.com/khanlab/bids-validator /src
cd /src
TAG=0.25.0
git checkout $TAG
sed -i -E "s/0.0.0/$TAG/" package.json
npm install -g /src
rm -f /src

#install octave
apt-get update
apt-get install -y octave

#add path for octave code
echo addpath\(genpath\(\'/opt/tar2bids/etc/octave\'\)\)\; >> /etc/octave.conf 


%runscript
exec /opt/tar2bids/tar2bids $@
