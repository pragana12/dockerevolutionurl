# Utiliza imagem base do Python
FROM python:3.9-slim

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Atualiza chaves GPG e instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ca-certificates \
    gnupg \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138 \
    && apt-get update && apt-get install -y \
    supervisor \
    gcc \
    python3-dev \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala Playwright
RUN pip install playwright && \
    playwright install

# Configura supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia código da aplicação
COPY . .

# Configura diretório de trabalho
WORKDIR /app

# Expõe porta necessária
EXPOSE 8000

# Comando principal via supervisord
CMD ["/usr/bin/supervisord"]