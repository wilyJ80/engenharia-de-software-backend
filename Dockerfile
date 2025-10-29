# Use imagem oficial do Python
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app/src

# Copia requirements
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando padrão para rodar o uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
