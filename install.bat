@echo off
REM Script de instalación para Windows

echo ========================================
echo Sistema de Analisis de Datos Farmaceuticos
echo ========================================
echo.

REM Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor, instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python encontrado
echo.

REM Crear entorno virtual
echo Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe
) else (
    python -m venv venv
    echo Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo.

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip
echo.

REM Instalar dependencias
echo Instalando dependencias...
echo Esto puede tardar unos minutos...
pip install -r requirements.txt
echo Dependencias instaladas
echo.

REM Crear archivo .env
if not exist .env (
    echo Creando archivo de configuracion...
    copy .env.example .env
    echo Archivo .env creado
) else (
    echo Archivo .env ya existe
)
echo.

REM Crear directorios
echo Creando directorios...
if not exist data\uploads mkdir data\uploads
if not exist data\examples mkdir data\examples
type nul > data\uploads\.gitkeep
echo Directorios creados
echo.

REM Verificar Ollama
echo Verificando Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo AVISO: Ollama no esta instalado
    echo.
    echo Para usar el asistente IA, descarga Ollama desde:
    echo https://ollama.ai/download
    echo.
    echo Despues ejecuta: ollama pull mistral
) else (
    echo Ollama instalado
    echo.
    set /p download="Descargar modelo Mistral ahora? (s/n): "
    if /i "%download%"=="s" (
        echo Descargando modelo Mistral...
        ollama pull mistral
        echo Modelo descargado
    )
)
echo.

REM Generar datos de ejemplo
set /p generate="Generar datos de ejemplo? (s/n): "
if /i "%generate%"=="s" (
    python -c "import pandas as pd; import numpy as np; np.random.seed(42); n=500; df=pd.DataFrame({'fecha': pd.date_range('2023-01-01', periods=n, freq='D'), 'ventas_euros': np.random.normal(1500, 300, n), 'num_clientes': np.random.poisson(50, n), 'categoria': np.random.choice(['Medicamentos', 'Cosmetica', 'Higiene', 'Nutricion'], n), 'prescripcion': np.random.choice(['Si', 'No'], n, p=[0.6, 0.4]), 'satisfaccion': np.random.randint(1, 6, n), 'edad_promedio': np.random.normal(45, 15, n), 'temperatura': np.random.normal(20, 5, n)}); df['ventas_euros'] = df['ventas_euros'] + df['num_clientes'] * 10 + np.random.normal(0, 100, n); df.to_csv('data/examples/farmacia_ejemplo.csv', index=False); print('Datos de ejemplo generados')"
)
echo.

echo ========================================
echo Instalacion completada!
echo.
echo Proximos pasos:
echo   1. Activa el entorno virtual:
echo      venv\Scripts\activate.bat
echo.
echo   2. Inicia la aplicacion:
echo      streamlit run app.py
echo.
echo   3. Abre tu navegador en:
echo      http://localhost:8501
echo.
echo ========================================
pause
