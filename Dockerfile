FROM python:3.11-slim

WORKDIR /app

COPY homepage-editor.py .

RUN pip install --no-cache-dir flask pyyaml

ENV YAML_FILE=/data/settings.yaml
ENV PORT=5000
ENV HOST=0.0.0.0

VOLUME /data

EXPOSE 5000

CMD ["python", "homepage-editor.py"]
