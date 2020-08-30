#FROM python:3.8
FROM centos/python-38-centos7:latest

WORKDIR /code

COPY requirements.txt .

RUN pip install --pre -r requirements.txt

COPY main.py .

ENTRYPOINT [ "python", "./main.py" ]