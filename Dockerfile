#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for license information.
#-------------------------------------------------------------------------------------------------------------

# Build image: docker build -t autogen-test .

# Run locally: docker run autogen-test
# Run in Docker: docker run -it -v ../test-autogen autogen-test:latest python ./my_app.py

FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

#
# Update the OS and maybe install packages
#
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
   && apt-get upgrade -y  \
   && apt-get -y install --no-install-recommends build-essential npm \
   && apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

# For docs
RUN npm install --global yarn
RUN pip install pydoc-markdown

# Import dependencies file
COPY requirements.txt /opt/app/requirements.txt

# Set working directory
WORKDIR /opt/app

# Install dependencies
RUN python -m pip install -r requirements.txt

# Import remaining project
COPY . /opt/app/

# Run script
CMD ["python", "./my_app.py"]