FROM ubuntu:latest
MAINTAINER Andruschenko "me@andrekovac.com"
RUN apt-get update -y
RUN apt-get install -y tar git curl nano build-essential
# RUN apt-get install -y python3.5 python-pip python3.5-dev build-essential python-numpy
RUN apt-get install -y python3.5 python3.5-dev python-distribute python-pip python-numpy
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install flask-restful
RUN pip install requests
RUN pip install simplejson

ENTRYPOINT ["python"]
CMD ["app.py"]