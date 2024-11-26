FROM python:3.11.9-slim as base

# Environment variables
ENV PYTHONUNBUFFERED=1

# Uvicorn configuration
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000
ENV UVICORN_RELOAD=true

RUN apt-get update \
    # dependencies for building Python packages && cleaning up unused files
    && apt-get install -y build-essential \
    libcurl4-openssl-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*


# Python dependencies
RUN pip install --upgrade pip setuptools

WORKDIR /app/

# Copy infrustructure scripts
COPY --chown=code:code ./compose/app/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

# Copy project
COPY ./ ./


# ************************************************
# ********** Development / QA  **********
# ************************************************
FROM base as development

RUN pip install -r requirements/main.txt

EXPOSE $UVICORN_PORT

CMD ["/start"]