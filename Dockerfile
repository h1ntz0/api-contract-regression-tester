FROM python:3.12-slim

WORKDIR /app

# Non-root user setup for security
RUN groupadd -r apitester && useradd -r -g apitester -d /app apitester

COPY pyproject.toml /app/
COPY src/ /app/src/
COPY templates/ /app/templates/

RUN pip install --no-cache-dir .

RUN chown -R apitester:apitester /app
USER apitester

ENTRYPOINT ["api-tester"]
CMD ["--help"]
