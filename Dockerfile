FROM neurodebian:bullseye
LABEL maintainer="<alik@robarts.ca>"

#heudiconv version:
ENV HEUDICONVTAG v0.5.4

#bids validator version:
ENV BIDSTAG 1.2.5

#pydeface version:
ENV PYDEFACETAG v1.1.0

#from heudiconv Dockerfile (neurodocker):

ARG DEBIAN_FRONTEND="noninteractive"

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    ND_ENTRYPOINT="/neurodocker/startup.sh"

# install heudiconv
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        heudiconv=0.9.0-1~nd110+1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install BIDS Validator
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        nodejs=12.22.5~dfsg-2~11u1 \
        npm=7.5.2+ds-2 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN npm install -g bids-validator@1.9.3

# install GNU parallel
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        locales=2.31-13+deb11u3 \
        parallel=20161222-1.1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "LANG=en_US.UTF-8" > /etc/locale.conf \
    && echo "LC_ALL=en_US.UTF-8" >> /etc/locale.conf \
    && locale-gen en_US.UTF-8

# install FSL flirt and fslorient
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        libxml2-dev=2.9.10+dfsg-6.7+deb11u1 \
        libopenblas-dev=0.3.13+ds-3 \
        python3-pip=20.3.4-4+deb11u1 \
        python3-setuptools=52.0.0-4 \
        wget=1.21-1+deb11u1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install --no-cache-dir pytest===3.6.0 networkx==2.0
ENV FSLDIR /opt/fsl
ENV FSLOUTPUTTYPE NIFTI_GZ
RUN mkdir -p $FSLDIR/bin \
    && wget -q -O $FSLDIR/bin/flirt https://www.dropbox.com/s/3wf2i7eiosoi8or/flirt \
    && wget -q -O $FSLDIR/bin/fslorient https://www.dropbox.com/s/t4grjp9aixwm8q9/fslorient \
    && chmod a+x $FSLDIR/bin/*
ENV PATH $FSLDIR/bin:$PATH

# install pydeface
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        git=1:2.30.2-1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && git clone https://github.com/poldracklab/pydeface /src/pydeface \
    && git -C /src/pydeface checkout v1.1.0
WORKDIR /src/pydeface
RUN python3 /src/pydeface/setup.py install
WORKDIR /

# install tar2bids
RUN mkdir -p /opt/tar2bids
COPY . /opt/tar2bids

# set up env vars
ENV LANGUAGE "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"
ENV LANG "en_US.UTF-8"

ENV PYTHONPATH $PYTHONPATH:/opt/tar2bids/heuristics

ENTRYPOINT ["/opt/tar2bids/tar2bids"]
