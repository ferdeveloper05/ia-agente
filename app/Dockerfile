# Imagen base ligera con Python
FROM python:3.11-bullseye

# Evita archivos .pyc y asegura logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias

# Copia dependencias primero
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto de la app
EXPOSE 8000

# Comando por defecto (ejemplo con FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
