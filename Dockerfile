# FROM <image>:<tag>, base image,
# default distributive for python is Linux Debian
FROM python:3.7-slim
# base image must contain required utilities
RUN mkdir /app
# from local to container dir, to skip files,
# create and register in .dockerignore
COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY api_yamdb /app
# dir for all following commands RUN, CMD, COPY, works like 'cd'
WORKDIR /app
# starts smth, e.g. bash-script or app server upon container start
# only one instruction is acceptable, latest is run,
# elems only in double quotes - JSON format
# file - args - command - params
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]

LABEL author='rock4ts' version=1

# ENV - sets virtual environment params on separate lines
# ENV <key>=<value>

