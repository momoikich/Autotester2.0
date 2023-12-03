FROM openjdk:11-jdk-slim

# copy the code source
COPY . .

# Install Git
RUN apt-get update && apt-get install -y git

# Install Python 3 and pip
RUN apt-get install -y python3 python3-pip

# Install Jinja
RUN pip3 install jinja2

# install gettext-base, curl, and jq
RUN apt-get install gettext-base && apt-get install -y curl jq

CMD ["/bin/bash"]
