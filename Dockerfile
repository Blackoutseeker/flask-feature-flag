FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Atualiza pacotes base do sistema operacional para corrigir vulnerabilidades antes do teste do Trivy
RUN apt-get update && \
    apt-get upgrade -y && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
