# start from existing ubuntu
FROM ubuntu:15.10
# update the package list
RUN apt-get update
#upgrade
RUN apt-get upgrade -y
# install node, node package manager and git
RUN apt-get -y install nodejs npm git
# make sure node is available to forever 
RUN ln -s /usr/bin/nodejs /usr/local/bin/node
# install express.js
RUN npm install express
# install forever globally
RUN npm install forever -g
# create a directory and git pull code into it
RUN mkdir /home/ubuntu
RUN git clone https://github.com/pzfreo/auto-deploy-node-js.git /home/ubuntu/auto-deploy-node-js
# expose port 8080
EXPOSE 8080
# run simpletest.js using forever
ENTRYPOINT forever /home/ubuntu/auto-deploy-node-js/simpletest.js

