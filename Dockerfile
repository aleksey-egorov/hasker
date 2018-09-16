# our base image
FROM ubuntu

RUN apt update
#RUN apt -y -q install git
RUN apt-get -y -q install make

# specify the port number the container should expose
EXPOSE 8080

WORKDIR /home/work

