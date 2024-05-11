FROM registry.access.redhat.com/ubi8/python-311:1-56.1712880527

LABEL Project="Herringbone"
LABEL Version="A-1.0.0"
LABEL Tool="Identifier"

EXPOSE 7000

WORKDIR /herringbone/identifier
COPY . .

CMD ["python3", "identifier.py"]