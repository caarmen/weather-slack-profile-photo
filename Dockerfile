FROM python:3.11.3-slim

WORKDIR /app

COPY requirements/prod.txt requirements.txt

RUN pip install -r requirements.txt

COPY wspp wspp
COPY resources resources

CMD python -m wspp.main
