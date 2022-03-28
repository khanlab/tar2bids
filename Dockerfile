FROM neurodebian:xenial
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
RUN export ND_ENTRYPOINT="/neurodocker/startup.sh" \
    && apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           apt-utils \
           bzip2 \
           ca-certificates \
           curl \
           locales \
           unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG="en_US.UTF-8" \
    && chmod 777 /opt && chmod a+s /opt \
    && mkdir -p /neurodocker \
    && if [ ! -f "$ND_ENTRYPOINT" ]; then \
         echo '#!/usr/bin/env bash' >> "$ND_ENTRYPOINT" \
    &&   echo 'set -e' >> "$ND_ENTRYPOINT" \
    &&   echo 'if [ -n "$1" ]; then "$@"; else /usr/bin/env bash; fi' >> "$ND_ENTRYPOINT"; \
    fi \
    && chmod -R 777 /neurodocker && chmod a+s /neurodocker

ENV DCM2NIIX_TAG="v1.0.20210317"

ENV PATH="/opt/dcm2niix-${DCM2NIIX_TAG}/bin:$PATH"
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           cmake \
           g++ \
           gcc \
           git \
           make \
           pigz \
           zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && git clone https://github.com/rordenlab/dcm2niix /tmp/dcm2niix \
    && cd /tmp/dcm2niix \
    && git fetch --tags \	
    && git checkout $DCM2NIIX_TAG \
    && mkdir /tmp/dcm2niix/build \
    && cd /tmp/dcm2niix/build \
    && cmake  -DCMAKE_INSTALL_PREFIX:PATH=/opt/dcm2niix-${DCM2NIIX_TAG} .. \
    && make \
    && make install \
    && rm -rf /tmp/dcm2niix

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           git \
           gcc \
           pigz \
           liblzma-dev \
           libc-dev \
           git-annex-standalone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


#checkout git heudiconv


RUN git clone https://github.com/nipy/heudiconv /src/heudiconv \
    && cd /src/heudiconv \
    && git fetch --tags \
    && git checkout $HEUDICONVTAG 


ENV CONDA_DIR="/opt/miniconda-latest" \
    PATH="/opt/miniconda-latest/bin:$PATH"
RUN export PATH="/opt/miniconda-latest/bin:$PATH" \
    && echo "Downloading Miniconda installer ..." \
    && conda_installer="/tmp/miniconda.sh" \
    && curl -fsSL --retry 5 -o "$conda_installer" https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash "$conda_installer" -b -p /opt/miniconda-latest \
    && rm -f "$conda_installer" \
    && conda install -yq -nbase conda=4.10.3 \
    && conda config --system --prepend channels conda-forge \
    && conda config --system --set auto_update_conda false \
    && conda config --system --set show_channel_urls true \
    && sync && conda clean -tipsy && sync \
    && conda install -y -q --name base \
           python=3.6 \
           traits>=4.6.0 \
           scipy \
           numpy \
           nomkl \
    && sync && conda clean -tipsy && sync \
    && bash -c "source activate base \
    &&  pip install pydicom dcmstack nipype nibabel && \
	pip install --no-cache-dir --editable \
             /src/heudiconv[all]" \
    && rm -rf ~/.cache/pip/* \
    && sync




#install rest

RUN mkdir -p /opt/tar2bids
COPY . /opt/tar2bids

## Install bids-validator



RUN apt-get update && \
    apt-get install -y curl git && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get remove -y curl && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN git clone https://github.com/bids-standard/bids-validator /opt/bids-validator && \
    cd /opt/bids-validator && \
    git checkout $BIDSTAG && \
    npm install -g /opt/bids-validator/bids-validator

#install gnu parallel
RUN apt-get update &&  apt-get install -y parallel


#install pydeface & deps, including FSL flirt (binary from dropbox)
RUN apt-get update && apt-get install -y python-setuptools libxml2-dev libopenblas-dev wget && pip install pytest==3.6.0 networkx==2.0
ENV FSLDIR /opt/fsl 
ENV FSLOUTPUTTYPE NIFTI_GZ
RUN mkdir -p $FSLDIR/bin && cd $FSLDIR/bin && wget https://www.dropbox.com/s/3wf2i7eiosoi8or/flirt && wget https://www.dropbox.com/s/t4grjp9aixwm8q9/fslorient && chmod a+x $FSLDIR/bin/*
ENV PATH $FSLDIR/bin:$PATH
RUN cd /src && git clone https://github.com/poldracklab/pydeface && cd pydeface && git checkout $PYDEFACETAG && python setup.py install



#need the below to avoid warnings when running gnu-parallel
RUN apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf && \
    echo "LC_ALL=en_US.UTF-8" >> /etc/locale.conf && \
    locale-gen en_US.UTF-8

ENV LANGUAGE "en_US.UTF-8"
ENV LC_ALL "en_US.UTF-8"
ENV LANG "en_US.UTF-8"

ENV PYTHONPATH $PYTHONPATH:/opt/tar2bids/heuristics

ENTRYPOINT ["/opt/tar2bids/tar2bids"]
