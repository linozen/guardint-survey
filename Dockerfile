FROM python:3.9-slim-buster

RUN apt-get update \
    && apt-get install build-essential make gcc -y \
    && apt-get install dpkg-dev -y \
    && apt-get install libjpeg-dev -y \
    && apt-get upgrade -y

RUN useradd --create-home --uid 9000 nonroot
USER nonroot
WORKDIR /home/nonroot/app
COPY --chown=nonroot:nonroot . .
ENV PATH="/home/nonroot/.local/bin:${PATH}"
RUN python3 -m pip install --user pipenv
RUN pipenv install

USER root
RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get auto-remove -y \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local/lib/python3.9 -name "*.pyc" -type f -delete

USER nonroot
EXPOSE 8501-8503
ENTRYPOINT [ "pipenv", "run" ]
