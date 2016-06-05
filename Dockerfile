FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"
RUN apt-get update && apt-get install -y mysql-client libmysqlclient-dev
RUN mkdir /chirp
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /chirp

WORKDIR /chirp
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]