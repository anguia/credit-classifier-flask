FROM ubuntu:16.10

ENV DEBIAN_FRONTEND noninteractive

COPY nginx/flask.conf /etc/nginx/sites-available/
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY app /var/www/app

RUN apt-get update && apt-get install -y \
    python-pip python-dev \
    supervisor uwsgi-plugin-python nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/log/nginx/app /var/log/uwsgi/app /var/log/supervisor \
    && rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    && pip install -r /var/www/app/requirements.txt \
    && chown -R www-data:www-data /var/www/app \
    && chown -R www-data:www-data /var/log

CMD ["/usr/bin/supervisord"]
