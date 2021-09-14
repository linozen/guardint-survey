FROM bitnami/python:3.9 as base
WORKDIR /app

# Install some build dependencies
RUN install_packages build-essential make gcc dpkg-dev libjpeg-dev sudo dbus-tests

# Set path and install poetry in it
ENV PATH /root/.local/bin:$PATH
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# We don't need poetry to create virtual environments; global site is just fine
RUN poetry config virtualenvs.create false

# Install project dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install

# Copy files
COPY . .

# Expoe ports and provide entrypoint
EXPOSE 8501-8503
ENTRYPOINT [ "poetry", "run" ]
