#  creates a layer from the ubuntu:18.04 Docker image.
FROM ubuntu:18.04

WORKDIR /app

# to resynchronize the package index files from their sources.
RUN apt -qq update

# http://bugs.python.org/issue19846
# https://github.com/SpEcHiDe/PublicLeech/pull/97
ENV LANG C.UTF-8

# sets the TimeZon, to be used inside the container
ENV TZ Asia/Kolkata

# we don't have an interactive xTerm
ENV DEBIAN_FRONTEND noninteractive

# install required packages
RUN apt -qq install -y curl git gnupg2 wget \
    apt-transport-https \
    python3 python3-pip \
    coreutils aria2 jq pv \
    ffmpeg mediainfo rclone

# each instruction creates one layer
# Only the instructions RUN, COPY, ADD create layers.
# copies 'requirements', to inside the container
COPY requirements.txt .

# install requirements, inside the container
RUN pip3 install --no-cache-dir -r requirements.txt

# adds files from your Docker client’s current directory.
COPY . .

# specifies what command to run within the container.
CMD ["python3", "-m", "tobrot"]
