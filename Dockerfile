FROM python:3.6

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt install -y git ruby-dev nodejs && \
    gem install compass sass && \
    npm -g install less && \
    apt-get update && \
    apt-get -y install \
        python3-pip \
	python3-dev \
        python3-pip \
        python-lxml \
        nginx

ENV PYTHONUNBUFFERED 1

RUN mkdir /crm

WORKDIR /crm

# Intall dependencies
COPY . .

  RUN pip3 install -r requirements.txt

  RUN pip3 install gunicorn reportlab

  RUN python3 manage.py collectstatic  --noinput

  pip3 install --no-cache-dir redis

ENV LANG C.UTF-8

ENV LC_ALL C.UTF-8

EXPOSE 80

COPY deploy/django_nginx.conf /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN rm -rf deploy && rm -rf Dockerfile && sed -i -e 's/www-data/root/g' /etc/nginx/nginx.conf

ENTRYPOINT ["sh", "entrypoint.sh"]
