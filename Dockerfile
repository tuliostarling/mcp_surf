FROM python:3.13-alpine

WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
  build-base \
  libffi-dev \
  musl-dev \
  gcc \
  g++ \
  make \
  linux-headers \
  postgresql-dev \
  rust \
  cargo \
  curl \
  bash

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 8000
EXPOSE 9000

CMD ["python", "__main__.py"]
