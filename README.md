# 💊 Análisis de Datos Farmacéuticos

Sistema de análisis estadístico interactivo y minimalista para servicios de farmacia, con cumplimiento total de RGPD.

## 🎯 Dos Versiones Disponibles

### 🌐 Versión HTML (Sin instalación)
**¡Abre y usa en 30 segundos!** → [Ver instrucciones](web/README.md)
- ✅ Sin instalación de software
- ✅ Funciona en cualquier navegador
- ✅ Análisis básicos e intermedios
- ✅ Ideal para uso rápido

### 🐍 Versión Streamlit (Completa)
**Sistema avanzado con IA y ML** → Continúa leyendo
- ✅ Análisis estadísticos avanzados
- ✅ Machine Learning (Random Forest, PCA)
- ✅ Asistente IA generativo local (Ollama)
- ✅ Soporte para datasets grandes
- ✅ Integración con R (opcional)

## 🌟 Características

### ✅ Cumplimiento RGPD
- **100% Local**: Todos los datos se procesan en tu equipo
- **Sin nube**: No se envía información a servidores externos
- **Auto-eliminación**: Los archivos se borran al cerrar la sesión
- **Privacidad total**: No se almacenan datos personales

### 📊 Análisis Disponibles

#### Análisis Exploratorio
- Estadísticas descriptivas completas
- Visualizaciones interactivas (histogramas, box plots, scatter plots)
- Detección automática de tipos de variables
- Análisis de valores nulos y duplicados

#### Análisis Estadístico
- **Correlaciones**: Pearson, Spearman, Kendall
- **Pruebas de hipótesis**: t-Student, ANOVA, Chi-cuadrado
- **Regresión**: Lineal simple y múltiple
- **Test de normalidad**: Shapiro-Wilk, Kolmogorov-Smirnov
- **Clustering**: K-means con visualización
- **PCA**: Análisis de componentes principales

#### Modelos Predictivos
- Random Forest para regresión y clasificación
- Validación automática (train/test split)
- Importancia de variables
- Métricas de rendimiento (R², RMSE, Accuracy)

### 🤖 Asistente IA Generativo (Local)

- **Interpretación automática** de resultados estadísticos
- **Sugerencias inteligentes** de análisis según objetivos
- **Chat interactivo** para consultas
- **Explicación de conceptos** estadísticos
- **Powered by Ollama** (ejecutado localmente)

### 📈 Visualizaciones Interactivas

Todas las visualizaciones son interactivas gracias a Plotly:
- Histogramas y distribuciones
- Gráficos de dispersión 2D y 3D
- Mapas de calor de correlaciones
- Box plots y violin plots
- Series temporales con descomposición
- Gráficos circulares y de barras

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Básica

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/data_fh.git
cd data_fh

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Activar en Linux/Mac:
source venv/bin/activate

# Activar en Windows:
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear archivo de configuración
cp .env.example .env
```

### Instalación del Asistente IA (Opcional pero recomendado)

Para usar el asistente IA generativo local:

```bash
# 1. Instalar Ollama
# Descarga desde: https://ollama.ai/download

# 2. Descargar modelo (Mistral recomendado)
ollama pull mistral

# 3. Verificar que funciona
ollama run mistral
```

**Modelos alternativos:**
- `ollama pull llama2` - Más ligero
- `ollama pull codellama` - Especializado en código
- `ollama pull neural-chat` - Conversacional

### Instalación de R (Opcional)

Para análisis estadísticos avanzados con R:

```bash
# Ubuntu/Debian
sudo apt-get install r-base

# macOS (con Homebrew)
brew install r

# Windows: Descargar desde https://cran.r-project.org/

# Instalar paquete Python para R
pip install rpy2
```

## 📖 Uso

### Iniciar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Flujo de Trabajo

1. **Cargar Datos**
   - Haz clic en "Cargar Datos" en el panel lateral
   - Selecciona tu archivo CSV o Excel
   - O usa los datos de ejemplo

2. **Explorar Datos**
   - Ve a la pestaña "Exploración"
   - Revisa estadísticas y visualizaciones

3. **Análisis Estadístico**
   - Selecciona el tipo de análisis
   - Elige las variables
   - Obtén resultados e interpretación

4. **Modelos Predictivos**
   - Define variable objetivo y predictoras
   - Entrena el modelo
   - Evalúa el rendimiento

5. **Asistente IA**
   - Pregunta sobre tus datos
   - Solicita sugerencias de análisis
   - Obtén explicaciones de conceptos

6. **Exportar**
   - Descarga resultados en CSV o Excel
   - Los datos permanecen en tu equipo

## 📁 Estructura del Proyecto

```
data_fh/
├── app.py                      # Aplicación principal Streamlit
├── config.py                   # Configuración
├── requirements.txt            # Dependencias
├── .env.example               # Plantilla de configuración
├── README.md                  # Este archivo
│
├── modules/                   # Módulos de análisis
│   ├── __init__.py
│   ├── data_processor.py      # Procesamiento de datos
│   ├── statistical_analyzer.py # Análisis estadístico
│   ├── ai_assistant.py        # Asistente IA
│   └── visualizations.py      # Visualizaciones
│
├── data/                      # Datos (gitignored por RGPD)
│   ├── uploads/              # Archivos subidos (temporal)
│   └── examples/             # Datos de ejemplo
│
└── docs/                      # Documentación adicional
    ├── guia_usuario.md
    ├── ejemplos_uso.md
    └── faq.md
```

## 🔒 Seguridad y RGPD

### Cumplimiento Normativo

Esta aplicación cumple con el Reglamento General de Protección de Datos (RGPD):

- ✅ **Artículo 5**: Principios relativos al tratamiento (minimización, integridad)
- ✅ **Artículo 25**: Protección de datos desde el diseño
- ✅ **Artículo 32**: Seguridad del tratamiento

### Medidas de Seguridad

1. **Procesamiento Local**: Todo se ejecuta en tu máquina
2. **Sin transmisión de datos**: No hay conexiones a servidores externos
3. **Auto-eliminación**: Los archivos temporales se borran automáticamente
4. **Sin logs de datos sensibles**: No se registran datos personales
5. **IA Local**: Ollama se ejecuta completamente offline

### Recomendaciones Adicionales

- No subir datos con información personal identificable sin anonimizar
- Usar en red privada o sin conexión a internet
- Realizar backups cifrados si es necesario
- Cerrar sesión correctamente al finalizar

## 📊 Ejemplos de Uso

### Ejemplo 1: Análisis de Ventas

```python
# Datos necesarios: fecha, ventas, categoría
# Análisis sugerido:
# 1. Estadísticas descriptivas de ventas
# 2. Comparación de medias por categoría (ANOVA)
# 3. Serie temporal de ventas
# 4. Predicción de ventas futuras
```

### Ejemplo 2: Control de Calidad

```python
# Datos necesarios: lote, resultado, fecha
# Análisis sugerido:
# 1. Test de normalidad
# 2. Control estadístico de procesos
# 3. Detección de outliers
# 4. Clustering de lotes problemáticos
```

### Ejemplo 3: Satisfacción de Clientes

```python
# Datos necesarios: satisfacción, factores varios
# Análisis sugerido:
# 1. Correlaciones entre factores y satisfacción
# 2. Regresión múltiple
# 3. Chi-cuadrado para variables categóricas
# 4. Modelo predictivo de satisfacción
```

## 🛠️ Configuración Avanzada

### Personalizar Ollama

Edita `.env`:

```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral  # o llama2, codellama, etc.
```

### Ajustar Límites

```bash
MAX_FILE_SIZE_MB=100
DATA_RETENTION_DAYS=0  # 0 = eliminar inmediatamente
```

### Configuración Estadística

En `config.py`:

```python
CONFIDENCE_LEVEL = 0.95  # Nivel de confianza (95%)
SIGNIFICANCE_LEVEL = 0.05  # Nivel de significancia (α = 0.05)
```

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo [Licencia MIT](LICENSE).

## 🆘 Soporte

### Problemas Comunes

**Error: "Ollama no disponible"**
- Instala Ollama: https://ollama.ai/download
- Ejecuta: `ollama run mistral`
- Reinicia la aplicación

**Error al cargar archivos grandes**
- Aumenta `MAX_FILE_SIZE_MB` en `.env`
- Considera dividir el archivo

**Visualizaciones no se muestran**
- Verifica que Plotly esté instalado: `pip install plotly`
- Actualiza el navegador

### Contacto

- Issues: [GitHub Issues](https://github.com/tu-usuario/data_fh/issues)
- Documentación: [Wiki del proyecto](https://github.com/tu-usuario/data_fh/wiki)

## 📚 Recursos Adicionales

### Documentación Estadística
- [Interpretación de p-valores](docs/p_valores.md)
- [Guía de pruebas estadísticas](docs/pruebas_estadisticas.md)
- [Machine Learning en farmacia](docs/ml_farmacia.md)

### Tutoriales
- [Video: Primeros pasos](https://youtube.com/...)
- [Tutorial completo PDF](docs/tutorial.pdf)
- [Casos de estudio](docs/casos_estudio.md)

## 🎯 Roadmap

### Versión 2.0
- [ ] Integración con bases de datos SQL
- [ ] Reportes automáticos en PDF
- [ ] Más modelos de ML (XGBoost, LightGBM)
- [ ] Series temporales avanzadas (Prophet)
- [ ] Dashboard en tiempo real

### Versión 3.0
- [ ] Análisis de texto con NLP
- [ ] Detección de anomalías automatizada
- [ ] Recomendaciones personalizadas
- [ ] API REST para integración

## ⭐ Agradecimientos

- [Streamlit](https://streamlit.io/) - Framework de UI
- [Plotly](https://plotly.com/) - Visualizaciones
- [Ollama](https://ollama.ai/) - IA generativa local
- [scikit-learn](https://scikit-learn.org/) - Machine Learning
- [pandas](https://pandas.pydata.org/) - Análisis de datos

---

**Hecho con ❤️ para profesionales de farmacia**

*Última actualización: 2024*
