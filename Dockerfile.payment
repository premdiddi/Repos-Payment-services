FROM ubuntu:16.04 as repos_payment
RUN apt-get update --fix-missing
RUN apt-get install openssl libssl1.0 build-essential tmux git lynx lsof nano htop curl -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python3.6 -y
RUN apt-get install python3-dev python-pip python3-pip -y
RUN apt-get install python-dev python3.6-dev -y
RUN apt-get install python-setuptools -y
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.6 /usr/bin/python3
RUN python3 --version
RUN mkdir /home/ubuntu
WORKDIR /home/ubuntu/
COPY req.txt .
RUN pip install -r req.txt
COPY . .
EXPOSE 5000
CMD python app.py
