FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -U pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

WORKDIR /app
COPY pyproject.toml  ./
RUN pip install --no-cache-dir .

COPY . ./

ENTRYPOINT ["python", "-m", "wyoming_piper_normalize"]