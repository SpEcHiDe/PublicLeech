#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  Copyright (C) 2020 PublicLeech Authors

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

#  creates a layer from the base Docker image.
FROM python:3.9.5-slim-buster

WORKDIR /app

# https://shouldiblamecaching.com/
ENV PIP_NO_CACHE_DIR 1

# http://bugs.python.org/issue19846
# https://github.com/SpEcHiDe/PublicLeech/pull/97
ENV LANG C.UTF-8

# we don't have an interactive xTerm
ENV DEBIAN_FRONTEND noninteractive

# sets the TimeZone, to be used inside the container
ENV TZ Asia/Kolkata

# fix "ephimeral" / "AWS" file-systems
RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# to resynchronize the package index files from their sources.
RUN apt -qq update

# base required pre-requisites before proceeding ...
RUN apt -qq install -y --no-install-recommends \
    curl \
    git \
    gnupg2 \
    unzip \
    wget \
    # install gcc [ PEP 517 ]
    build-essential gcc \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/* && \
    apt-add-repository non-free

# add required files to sources.list
RUN wget -q -O - https://mkvtoolnix.download/gpg-pub-moritzbunkus.txt | apt-key add - && \
    wget -qO - https://ftp-master.debian.org/keys/archive-key-10.asc | apt-key add -
RUN sh -c 'echo "deb https://mkvtoolnix.download/debian/ buster main" >> /etc/apt/sources.list.d/bunkus.org.list' && \
    sh -c 'echo deb http://deb.debian.org/debian buster main contrib non-free | tee -a /etc/apt/sources.list'

# to resynchronize the package index files from their sources.
RUN apt -qq update

# install required packages
RUN apt -qq install -y --no-install-recommends \
    # this package is required to fetch "contents" via "TLS"
    apt-transport-https \
    # install coreutils
    coreutils aria2 jq pv \
    # install encoding tools
    ffmpeg \
    # install extraction tools
    mkvtoolnix \
    p7zip rar unrar zip \
    # miscellaneous helpers
    megatools mediainfo rclone && \
    # clean up previously installed SPC
    apt purge -y software-properties-common && \
    # clean up the container "layer", after we are done
    rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

# each instruction creates one layer
# Only the instructions RUN, COPY, ADD create layers.
# copies 'requirements', to inside the container
# ..., there are multiple '' dependancies,
# requiring the use of the entire repo, hence
# adds files from your Docker client’s current directory.
COPY . .

# install requirements, inside the container
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# specifies what command to run within the container.
CMD ["python3", "-m", "publicleechgroup"]
