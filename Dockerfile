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
WORKDIR /chirp

# for cache
# Configure Nginx and uwsgi
ADD ./requirements.txt /chirp/requirements.txt
RUN rm /etc/nginx/sites-enabled/default
ADD ./.deploy/nginx.conf /etc/nginx/sites-enabled/chirp.conf
ADD ./.deploy/supervisord.conf /etc/supervisor/conf.d/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /chirp

EXPOSE 80
# CMD ["supervisord", "-n"]
CMD ["sh", "./.deploy/init.sh"]


