#!/bin/bash
docker run -p 80:80 -d -P -v /home/admin/master/testsite:/usr/share/nginx/html \
--name testsite nginx
