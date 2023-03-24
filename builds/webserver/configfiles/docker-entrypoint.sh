#!/bin/bash

chown apache:apache /usr/share/nginx/html/*.php
mkdir -p /run/php-fpm/
/usr/sbin/nginx
/usr/sbin/php-fpm -F
