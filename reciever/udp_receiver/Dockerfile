FROM registry.access.redhat.com/ubi8/python-311:1-56.1712880527

LABEL Project="Herringbone"
LABEL Version="A-2.1.1"
LABEL Tool="UDP Receiver"

EXPOSE 7002/udp

USER root

WORKDIR /herringbone/receiver

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "udp_receiver.py"]