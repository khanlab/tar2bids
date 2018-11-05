#FROM khanlab/heudiconv:latest
FROM neurodebian:xenial
MAINTAINER <alik@robarts.ca>

#bids validator version:
ENV TAG 1.0.5

RUN apt-get update && apt-get install -y heudiconv

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
