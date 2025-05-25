FROM python:3.12-slim AS base

ENV DATASCIENCE_USER=datascience
ENV DATASCIENCE_UID=1000
ENV HOME=/home/${DATASCIENCE_USER}

# Create a non-root user
RUN useradd --create-home --uid ${DATASCIENCE_UID} ${DATASCIENCE_USER}
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir oci oracle-ads


FROM base AS file-size-checker
COPY app/ /app
WORKDIR /app
RUN chown -R ${DATASCIENCE_USER}:${DATASCIENCE_USER} /app
USER ${DATASCIENCE_USER}
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python","-u","/app/process_batch.py"]


FROM file-size-checker AS final
