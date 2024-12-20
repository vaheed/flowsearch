FROM python:3.9-slim AS builder

RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make sure you're copying your source code into the image
COPY src/ /app/src/

FROM python:3.9-slim
RUN useradd -m appuser
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app
USER appuser
WORKDIR /app
CMD ["/bin/bash"]
