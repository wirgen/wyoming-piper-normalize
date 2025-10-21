FROM python:3.11-slim-bookworm

RUN pip3 install --no-cache-dir -U \
        setuptools \
        wheel

RUN pip3 install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu

WORKDIR /app

COPY pyproject.toml /app

RUN pip3 install --no-cache-dir .

COPY . /app

ENTRYPOINT ["python", "-m", "wyoming_piper_normalize"]