FROM bitnami/python:3.9-prod
WORKDIR /app

# Install some build dependencies
RUN install_packages \
    build-essential \
    libjpeg-dev

# Install project dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Switch to non-root user
RUN adduser \
    --shell "/sbin/nologin" \
    --no-create-home \
    --gecos "nonroot" \
    --disabled-password nonroot
USER nonroot

# Copy files
COPY --chown=nonroot:nonroot . .

# Expose ports and provide entrypoint
EXPOSE 8501
