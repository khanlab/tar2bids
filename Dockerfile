#FROM khanlab/heudiconv:latest
FROM neurodebian:xenial
MAINTAINER <alik@robarts.ca>

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

ENV DCM2NIIX_DATE=20181112
ENV DCM2NIIX_SHA="62f3b6e801e65aa61484b8e533ab38d284962a70"

ENV PATH="/opt/dcm2niix-v1.0.${DCM2NIIX_DATE}/bin:$PATH"
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
    && git checkout $DCM2NIIX_SHA \
    && mkdir /tmp/dcm2niix/build \
    && cd /tmp/dcm2niix/build \
    && cmake  -DCMAKE_INSTALL_PREFIX:PATH=/opt/dcm2niix-v1.0.${DCM2NIIX_DATE} .. \
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
    && git checkout v0.5.1 


ENV CONDA_DIR="/opt/miniconda-latest" \
    PATH="/opt/miniconda-latest/bin:$PATH"
RUN export PATH="/opt/miniconda-latest/bin:$PATH" \
    && echo "Downloading Miniconda installer ..." \
    && conda_installer="/tmp/miniconda.sh" \
    && curl -fsSL --retry 5 -o "$conda_installer" https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash "$conda_installer" -b -p /opt/miniconda-latest \
    && rm -f "$conda_installer" \
    && conda update -yq -nbase conda \
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

#bids validator version:
ENV TAG 1.0.5

RUN apt-get update && \
    apt-get install -y curl git && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get remove -y curl && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN git clone https://github.com/bids-standard/bids-validator /opt/bids-validator && \
    cd /opt/bids-validator && \
    git checkout $TAG && \
    sed -i -E "s/0.0.0/$TAG/" package.json && \
    npm install -g /opt/bids-validator

#install gnu parallel
RUN apt-get update &&  apt-get install -y parallel


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
