FROM nginx:latest

RUN apt-get update && apt-get install -y certbot python-certbot-nginx

RUN rm -f /etc/nginx/conf.d/default.conf

WORKDIR /app

ADD portfolio.conf /app

ADD container_start.sh /app/container_start.sh

ENTRYPOINT ["sh", "container_start.sh"]
