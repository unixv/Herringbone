FROM registry.access.redhat.com/ubi8/python-311:1-56.1712880527

LABEL Project="Herringbone"
LABEL Version="A-1.0.0"
LABEL Tool="Parser"

EXPOSE 7005

USER root

WORKDIR /parser

COPY . .

CMD ["python3", "parser.py"]