FROM python:3.10-slim

WORKDIR /app

# Install dependencies and create certificate directory
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && mkdir -p /root/.postgresql \
    && rm -rf /var/lib/apt/lists/*

# Copy CA certificate to PostgreSQL's default location
COPY ./root.crt /root/.postgresql/root.crt
RUN chmod 0600 /root/.postgresql/root.crt

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY .env .

EXPOSE 8080

CMD ["sh", "-c", "alembic upgrade head && python3 src/main.py --log-level=DEBUG"]
