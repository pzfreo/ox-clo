FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install wget gnupg2 -y
RUN apt install apt-transport-https -y 
RUN wget -q -O - https://www.apache.org/dist/cassandra/KEYS | apt-key add -
RUN sh -c 'echo "deb http://www.apache.org/dist/cassandra/debian 311x main" > /etc/apt/sources.list.d/cassandra.list'
RUN apt update
RUN apt install cassandra -y

CMD ["/bin/sh", "-c", "while true; do echo hello; sleep 10;done"]

