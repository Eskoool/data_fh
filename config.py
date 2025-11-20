"""
Configuración de la aplicación
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Rutas
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
EXAMPLES_DIR = DATA_DIR / "examples"

# Crear directorios si no existen
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Configuración de la aplicación
APP_TITLE = os.getenv("APP_TITLE", "Análisis de Datos Farmacéuticos")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Sistema de análisis estadístico local compatible con RGPD")

# Ollama (IA generativa local)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# Límites de archivos
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "csv,xlsx,xls").split(",")

# RGPD
DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "0"))
AUTO_DELETE_UPLOADS = os.getenv("AUTO_DELETE_UPLOADS", "true").lower() == "true"

# Configuración estadística
CONFIDENCE_LEVEL = 0.95
SIGNIFICANCE_LEVEL = 0.05
