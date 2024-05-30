FROM registry.access.redhat.com/ubi8/python-311:1-56.1712880527

LABEL Project="Herringbone"
LABEL Version="A-1.1.2"
LABEL Tool="Identifier"

EXPOSE 7000

USER root

WORKDIR /identifier

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "identifier.py"]