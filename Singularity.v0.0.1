Bootstrap: shub
From: khanlab/heudiconv:0.4.3

%setup
mkdir -p $SINGULARITY_ROOTFS/opt/tar2bids
cp -Rv . $SINGULARITY_ROOTFS/opt/tar2bids

%post 

## Install bids-validator
apt-get update && \
apt-get install -y curl git && \
curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
apt-get remove -y curl && \
apt-get install -y nodejs && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

git clone http://github.com/khanlab/bids-validator /opt/bids-validator
cd /opt/bids-validator
TAG=0.25.0
git checkout $TAG
sed -i -E "s/0.0.0/$TAG/" package.json
npm install -g /opt/bids-validator

#install octave
apt-get update
apt-get install -y octave

#add path for octave code
echo addpath\(genpath\(\'/opt/tar2bids/etc/octave\'\)\)\; >> /etc/octave.conf 

#install gnu parallel 
apt-get update 
apt-get install -y parallel 

export LANGUAGE="en_US.UTF-8"
echo 'LANGUAGE="en_US.UTF-8"' >> /etc/default/locale
echo 'LC_ALL="en_US.UTF-8"' >> /etc/default/locale

%runscript
exec /opt/tar2bids/tar2bids $@
