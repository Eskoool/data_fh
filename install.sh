#!/bin/bash

# Script de instalación para el sistema de análisis de datos farmacéuticos
# Compatible con Linux y macOS

echo "🚀 Instalación del Sistema de Análisis de Datos Farmacéuticos"
echo "============================================================="
echo ""

# Verificar Python
echo "📌 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor, instálalo primero."
    echo "   https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"
echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "⚠️  El entorno virtual ya existe. ¿Deseas recrearlo? (s/n)"
    read -r response
    if [ "$response" = "s" ] || [ "$response" = "S" ]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi
echo "✅ Entorno virtual creado"
echo ""

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate
echo "✅ Entorno activado"
echo ""

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip actualizado"
echo ""

# Instalar dependencias
echo "📚 Instalando dependencias..."
echo "   Esto puede tardar unos minutos..."
pip install -r requirements.txt
echo "✅ Dependencias instaladas"
echo ""

# Crear archivo .env
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo de configuración..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
else
    echo "ℹ️  Archivo .env ya existe"
fi
echo ""

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p data/uploads
mkdir -p data/examples
touch data/uploads/.gitkeep
echo "✅ Directorios creados"
echo ""

# Verificar Ollama
echo "🤖 Verificando Ollama (IA Generativa)..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama instalado"
    echo ""
    echo "📥 ¿Deseas descargar el modelo Mistral ahora? (s/n)"
    echo "   (Tamaño: ~4GB, necesario para el asistente IA)"
    read -r response
    if [ "$response" = "s" ] || [ "$response" = "S" ]; then
        echo "⬇️  Descargando modelo Mistral..."
        ollama pull mistral
        echo "✅ Modelo Mistral descargado"
    else
        echo "ℹ️  Puedes descargarlo más tarde con: ollama pull mistral"
    fi
else
    echo "⚠️  Ollama no está instalado"
    echo ""
    echo "   El asistente IA no estará disponible sin Ollama."
    echo "   Para instalarlo:"
    echo "   - Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   - macOS: brew install ollama"
    echo "   - Windows: https://ollama.ai/download"
    echo ""
    echo "   Después ejecuta: ollama pull mistral"
fi
echo ""

# Generar datos de ejemplo
echo "📊 ¿Deseas generar datos de ejemplo? (s/n)"
read -r response
if [ "$response" = "s" ] || [ "$response" = "S" ]; then
    python3 -c "
import pandas as pd
import numpy as np

np.random.seed(42)
n = 500

df = pd.DataFrame({
    'fecha': pd.date_range('2023-01-01', periods=n, freq='D'),
    'ventas_euros': np.random.normal(1500, 300, n),
    'num_clientes': np.random.poisson(50, n),
    'categoria': np.random.choice(['Medicamentos', 'Cosmetica', 'Higiene', 'Nutricion'], n),
    'prescripcion': np.random.choice(['Si', 'No'], n, p=[0.6, 0.4]),
    'satisfaccion': np.random.randint(1, 6, n),
    'edad_promedio': np.random.normal(45, 15, n),
    'temperatura': np.random.normal(20, 5, n)
})

df['ventas_euros'] = df['ventas_euros'] + df['num_clientes'] * 10 + np.random.normal(0, 100, n)
df.to_csv('data/examples/farmacia_ejemplo.csv', index=False)
print('✅ Datos de ejemplo generados en data/examples/farmacia_ejemplo.csv')
"
fi
echo ""

# Finalizar
echo "============================================================="
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "   1. Activa el entorno virtual (si no está activo):"
echo "      source venv/bin/activate"
echo ""
echo "   2. Inicia la aplicación:"
echo "      streamlit run app.py"
echo ""
echo "   3. Abre tu navegador en:"
echo "      http://localhost:8501"
echo ""
echo "💡 Consejos:"
echo "   - Lee el README.md para más información"
echo "   - Usa datos de ejemplo para familiarizarte"
echo "   - Todos los datos se procesan localmente (RGPD)"
echo ""
echo "🆘 ¿Problemas? Consulta: https://github.com/tu-usuario/data_fh/issues"
echo ""
echo "============================================================="
