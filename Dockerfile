FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    libmysqlclient-dev \
    mysql-client \
    nginx \
    supervisor

RUN mkdir /chirp
ADD . /chirp

WORKDIR /chirp
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Configure Nginx and uwsgi
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /chirp/.deploy/nginx.conf /etc/nginx/sites-enabled/chirp.conf
RUN ln -s /chirp/.deploy/supervisord.conf /etc/supervisor/conf.d/

EXPOSE 80
CMD ["supervisord", "-n"]

