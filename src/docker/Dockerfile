ARG REGISTRY=docker.io
FROM python:3-slim
LABEL maintainer="dev_lau11@a.jlv6.com"
ENV WATCH_DIR=/media
ENV TRIGGER_SCRIPT=/scripts/trigger-jf-lib-scan.sh
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install watchdog
WORKDIR /app
COPY watcher.py .
VOLUME ["/scripts"]
CMD ["python", "watcher.py"]