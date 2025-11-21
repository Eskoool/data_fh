# 🚀 Inicio Rápido - Análisis de Datos Farmacéuticos

## ⚡ Opción 1: Versión HTML (RECOMENDADO PARA EMPEZAR)

### ¡Prueba en 30 segundos! 🎯

1. **Abre el archivo HTML en tu navegador**

   ```bash
   # Opción A: Navega y abre
   cd web/
   # Luego abre index.html con doble clic

   # Opción B: Desde terminal (Linux/Mac)
   open web/index.html

   # Opción C: Desde terminal (Windows)
   start web/index.html
   ```

2. **Usa datos de ejemplo**
   - Haz clic en "Usar Datos de Ejemplo"
   - ¡Ya tienes datos cargados!

3. **Explora las pestañas**
   - 📊 Estadísticas → Selecciona "ventas_euros" y calcula
   - 📈 Visualizaciones → Crea un histograma
   - 🔗 Correlaciones → Calcula matriz de correlación
   - 🧪 Pruebas → Haz una prueba t

### ¿Qué puedes hacer?
✅ Estadísticas descriptivas completas
✅ Visualizaciones interactivas (histogramas, dispersión, barras)
✅ Correlaciones de Pearson
✅ Prueba t de Student
✅ Test de normalidad
✅ Detección de outliers
✅ Exportar resultados

### Ventajas
- ✅ **Cero instalación**
- ✅ **Funciona offline** (después de la primera carga)
- ✅ **100% privado** (todo en tu navegador)
- ✅ **Comparte fácilmente** (solo envía la carpeta `web/`)

---

## 🐍 Opción 2: Versión Streamlit (Análisis Avanzados)

### Instalación (5 minutos)

**Linux/macOS:**
```bash
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Iniciar

```bash
# 1. Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Ejecutar
streamlit run app.py

# 3. Abre tu navegador en http://localhost:8501
```

### ¿Qué puedes hacer ADEMÁS de la versión HTML?
✅ **Machine Learning** (Random Forest)
✅ **Clustering** (K-means) con visualización 3D
✅ **PCA** (Análisis de componentes principales)
✅ **Regresión múltiple** avanzada
✅ **ANOVA** con test post-hoc Tukey
✅ **Chi-cuadrado** para variables categóricas
✅ **Asistente IA** (con Ollama) para interpretar resultados
✅ **Series temporales** con descomposición
✅ Datasets **ilimitados** en tamaño

### Asistente IA (Opcional)

Para activar el asistente IA que interpreta resultados:

```bash
# 1. Instalar Ollama
# Descarga desde: https://ollama.ai/download

# 2. Descargar modelo
ollama pull mistral

# 3. Verificar
ollama list

# 4. Reiniciar la aplicación
streamlit run app.py
```

---

## 📊 ¿Cuál usar?

### Usa HTML si:
- ⚡ Quieres empezar **YA** sin instalar nada
- 📱 Necesitas algo **portable** (USB, enviar por email)
- 🔍 Análisis **básicos a intermedios** son suficientes
- 📉 Datasets **pequeños** (< 5,000 filas)
- 🌐 Quieres **compartir** fácilmente con colegas

### Usa Streamlit si:
- 🧠 Necesitas **Machine Learning** y análisis avanzados
- 🤖 Quieres el **asistente IA** para interpretar resultados
- 📊 Trabajas con **datasets grandes** (> 10,000 filas)
- 🔬 Necesitas **pruebas estadísticas** complejas (ANOVA, regresión múltiple)
- 📈 Análisis de **series temporales** avanzado

---

## 🎯 Ejemplos Rápidos

### Ejemplo 1: Ver distribución de ventas (HTML)

```
1. Abre web/index.html
2. Cargar datos de ejemplo
3. Pestaña "Visualizaciones"
4. Tipo: Histograma
5. Variable: ventas_euros
6. Generar Gráfico
```

### Ejemplo 2: Correlación entre variables (HTML)

```
1. Pestaña "Correlaciones"
2. Clic en "Calcular Correlaciones"
3. Observa la matriz coloreada
4. Verde = correlación alta
5. Rojo = correlación baja
```

### Ejemplo 3: Comparar dos grupos (HTML)

```
1. Pestaña "Pruebas Estadísticas"
2. Tipo: Prueba t
3. Variable numérica: ventas_euros
4. Variable categórica: prescripcion
5. Ejecutar
6. Resultado te dice si hay diferencia significativa
```

### Ejemplo 4: Predicción con ML (Streamlit)

```
1. Streamlit: http://localhost:8501
2. Cargar datos
3. Pestaña "Modelos Predictivos"
4. Tipo: Regresión
5. Objetivo: ventas_euros
6. Predictoras: num_clientes, satisfaccion
7. Entrenar Modelo
8. Ver importancia de variables
```

---

## 📁 Estructura del Proyecto

```
data_fh/
├── web/                    ← 🌐 VERSIÓN HTML (usa esta para empezar)
│   ├── index.html         ← Abre este archivo
│   ├── css/
│   ├── js/
│   └── README.md
│
├── app.py                 ← 🐍 Versión Streamlit (ejecuta con: streamlit run app.py)
├── modules/               ← Módulos Python
├── data/
│   └── examples/          ← Datos de ejemplo
├── docs/                  ← Documentación
│
├── install.sh             ← Instalador Linux/Mac
├── install.bat            ← Instalador Windows
└── README.md              ← Documentación completa
```

---

## 🆘 Ayuda Rápida

### HTML no carga
- Verifica que JavaScript esté habilitado
- Prueba con Chrome, Firefox o Edge
- Abre la consola (F12) y busca errores

### Streamlit no inicia
```bash
# Verificar Python
python --version  # Debe ser 3.8+

# Reinstalar dependencias
pip install -r requirements.txt

# Ejecutar con puerto diferente
streamlit run app.py --server.port 8502
```

### Archivo CSV da error
- Verifica que use **comas** como separador
- Primera fila debe tener **nombres de columnas**
- Guarda con codificación **UTF-8**

---

## 📞 Recursos

- 📖 [README completo](README.md)
- 🌐 [Guía HTML](web/README.md)
- ❓ [FAQ](docs/FAQ.md)
- 🚀 [Guía rápida](docs/guia_rapida.md)
- 🐛 [Reportar problema](https://github.com/Eskoool/data_fh/issues)

---

## 🎉 ¡Empieza Ahora!

**Recomendación:** Empieza con la versión HTML para familiarizarte, luego prueba Streamlit para funciones avanzadas.

```bash
# Paso 1: Prueba HTML
open web/index.html

# Paso 2 (más tarde): Prueba Streamlit
./install.sh
streamlit run app.py
```

**¡Buena suerte con tus análisis!** 💊📊

---

*Sistema de Análisis de Datos Farmacéuticos v1.0*
*100% Local • RGPD Compliant • Open Source*
