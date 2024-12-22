FROM registry.access.redhat.com/ubi8/python-311:1-56.1712880527

LABEL Project="Herringbone"
LABEL Version="Alpha 2.1.9"
LABEL Tool="UDP Receiver"

EXPOSE 7002/udp

USER root

WORKDIR /herringbone/receiver

COPY . .

RUN pip3 install -r requirements.txt
RUN chmod +x receiveradmin.py

CMD ["python3", "udp_receiver.py"]