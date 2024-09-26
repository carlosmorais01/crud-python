# Use uma imagem oficial do Python como base
FROM python:3.12.6

# Instalar as dependências do PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o resto dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta 5000 (a porta padrão do Flask)
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0"]
