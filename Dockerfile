FROM python:3.13.0b1-slim-bookworm

RUN apt update && apt install -y iproute2 tcpdump iputils-ping net-tools

RUN pip3 install scapy



