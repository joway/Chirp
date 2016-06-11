FROM python:3.5.1
MAINTAINER joway wong "joway.w@gmail.com"

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    libmysqlclient-dev \
    mysql-client \
    nginx \
    supervisor \

RUN mkdir /chirp
ADD . /chirp

WORKDIR /chirp
RUN pip install -r requirements.txt


# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /chirp/.deploy/nginx.conf /etc/nginx/sites-enabled/chirp.conf
RUN uwsgi --ini uwsgi.ini
RUN service nginx restart