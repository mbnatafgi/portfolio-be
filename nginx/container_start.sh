#!/bin/bash

certbot certonly --nginx -n --agree-tos -vvv --keep --expand \
  -d $DOMAIN,www.$DOMAIN \
  --email bilal.natafji@icloud.com \
  --logs-dir /portfolio-nginx/letsencrypt/logs \
  --config-dir /portfolio-nginx/letsencrypt/config

nginx -s quit

for file in /app/*.conf; do
  envsubst "`env | awk -F = '{printf \" \\\\$%s\", $1}'`" < $file > /etc/nginx/conf.d/$(basename $file);
done

nginx -g 'daemon off;'