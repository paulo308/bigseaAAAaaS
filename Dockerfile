# Base image
FROM alpine:3.4

WORKDIR /usr/src/app

# Installing needed packages
RUN apk add --update --no-cache python3 \
 && apk add --update --no-cache --virtual .build-deps gcc libc-dev python3 python3-dev

# Install requirements
ADD aaa_manager/requirements.txt /usr/src/app/aaa_manager/
RUN pip3 install --no-cache-dir -q --upgrade pip \
 && pip3 install --no-cache-dir -r aaa_manager/requirements.txt \
 && rm -rf ~/.cache/pip/*

# Run server. gunicorn -u is need for docker-compose (needs unbuffered output)
CMD python3 setup.py develop && gunicorn --reload --log-level DEBUG --paste development.ini
