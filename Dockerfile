FROM debian:bullseye
LABEL maintainer="<alik@robarts.ca>"

# dcm2niix version
ENV DCM2NIIXTAG v1.0.20210317

#heudiconv version:
ENV HEUDICONVTAG v0.5.4

#bids validator version:
ENV BIDSTAG 1.2.5

#pydeface version:
ENV PYDEFACETAG v1.1.0

ARG DEBIAN_FRONTEND="noninteractive"

# install dcm2niix
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        apt-utils=2.2.4 \
        ca-certificates=20210119 \
        locales=2.31-13+deb11u3 \
        pigz=2.6-1 \
        unzip=6.0-26 \
        wget=1.21-1+deb11u1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && mkdir /opt/dcm2niix \
    && wget -q -O /opt/dcm2niix/dcm2niix.zip https://github.com/rordenlab/dcm2niix/releases/download/${DCM2NIIXTAG}/dcm2niix_lnx.zip \
    && unzip /opt/dcm2niix/dcm2niix.zip -d /opt/dcm2niix \
    && rm /opt/dcm2niix/dcm2niix.zip
ENV PATH /opt/dcm2niix:$PATH


# install heudiconv
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        python3=3.9.2-3 \
        python3-pip=20.3.4-4+deb11u1 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && pip install --no-cache-dir heudiconv==${HEUDICONVTAG}


# install BIDS Validator
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
        nodejs=12.22.5~dfsg-2~11u1 \
        npm=7.5.2+ds-2 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN npm install -g bids-validator@${BIDSTAG}

# install GNU parallel
RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
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
    && git -C /src/pydeface checkout ${PYDEFACETAG}
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
