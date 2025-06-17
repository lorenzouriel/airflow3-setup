# Dockerfile
FROM apache/airflow:3.0.0

# Instala as dependências de sistema necessárias para python-ldap
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Troca para o usuário airflow para instalar Python packages
USER airflow

# Copia os requirements para dentro da imagem
COPY requirements.txt /requirements.txt

# Instala os requisitos Python
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r /requirements.txt

# Copia os patches (arquivos corrigidos)
USER root
ENV SITE_PACKAGES_DIR=/home/airflow/.local/lib/python3.12/site-packages
COPY --chown=airflow:airflow ./airflow-patch/ ${SITE_PACKAGES_DIR}/

USER airflow