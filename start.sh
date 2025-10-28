#!/bin/bash

# Script de inicio para producción
# Usar el puerto proporcionado por el entorno o 5000 por defecto
PORT=${PORT:-5000}

# Iniciar gunicorn con configuración de producción
gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
