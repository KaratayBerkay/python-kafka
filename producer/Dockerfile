FROM python:3.12.2-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /producer

# Install dependencies
COPY requirements.txt /tmp/requirements.txt

# Install dependencies
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt --no-cache-dir && \
    rm -rf /root/.cache/

# Set work directory
ADD /producer /producer

# Run the application
CMD ["python", "runner.py"]
