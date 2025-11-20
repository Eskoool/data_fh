# 🚀 Guía Rápida de Uso

## Inicio Rápido (5 minutos)

### 1. Instalación

```bash
# Linux/macOS
./install.sh

# Windows
install.bat
```

### 2. Iniciar Aplicación

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Iniciar aplicación
streamlit run app.py
```

### 3. Primer Análisis

1. **Cargar datos** → Click en "Usar Datos de Ejemplo"
2. **Explorar** → Pestaña "Exploración" para ver resumen
3. **Analizar** → Pestaña "Análisis Estadístico" → Seleccionar "Correlaciones"
4. **Interpretar** → Usar el asistente IA para entender resultados

## Casos de Uso Comunes

### 📊 Análisis de Ventas

**Objetivo**: Identificar factores que influyen en las ventas

**Pasos**:
1. Cargar archivo con columnas: `fecha`, `ventas`, `categoria`, `clientes`
2. Análisis → Correlaciones → Seleccionar variables numéricas
3. Análisis → Regresión Lineal → Variable objetivo: `ventas`
4. Asistente IA → "¿Qué variables son más importantes para las ventas?"

**Resultado**: Conocerás qué factores impactan más en tus ventas

---

### 🔬 Comparación de Grupos

**Objetivo**: Comparar medicamentos con y sin prescripción

**Pasos**:
1. Cargar datos con columnas: `ventas`, `tipo_medicamento`
2. Análisis → Prueba t de Student
3. Variable numérica: `ventas`
4. Variable categórica: `tipo_medicamento`

**Resultado**: Sabrás si hay diferencia significativa entre grupos

---

### 🎯 Predicción de Demanda

**Objetivo**: Predecir ventas futuras

**Pasos**:
1. Cargar histórico de ventas
2. Modelos Predictivos → Regresión
3. Variable objetivo: `ventas`
4. Variables predictoras: `dia_semana`, `mes`, `promocion`, etc.

**Resultado**: Modelo que predice ventas con métricas de precisión

---

### 📈 Análisis de Tendencias

**Objetivo**: Ver evolución temporal

**Pasos**:
1. Datos con columna de fecha
2. Exploración → Visualizaciones → Gráfico de líneas
3. Eje X: `fecha`
4. Eje Y: `ventas` o variable de interés

**Resultado**: Gráfico interactivo de tendencias

---

## Atajos de Teclado

| Acción | Atajo |
|--------|-------|
| Recargar app | `R` o `Ctrl+R` |
| Limpiar caché | `C` |
| Menú settings | `S` |
| Modo amplio | `W` |

## Tips Rápidos

### ✅ Mejores Prácticas

- **Limpia tus datos** antes de análisis complejos
- **Usa el asistente IA** para interpretar resultados
- **Exporta resultados** importantes inmediatamente
- **Prueba con datos de ejemplo** antes de usar datos reales

### ⚠️ Errores Comunes

**"Error al cargar archivo"**
- Verifica que el archivo sea CSV o Excel válido
- Comprueba que no tenga caracteres especiales en los nombres de columnas
- Asegúrate de que el tamaño sea menor a 100MB

**"Variable no encontrada"**
- Revisa los nombres exactos de las columnas
- Verifica que la columna tenga el tipo correcto (numérica/categórica)

**"Ollama no disponible"**
- Instala Ollama: https://ollama.ai/download
- Ejecuta: `ollama pull mistral`
- Reinicia la aplicación

### 🎨 Personalización

**Cambiar tema de gráficos**:
Edita en `modules/visualizations.py`:
```python
self.color_palette = px.colors.qualitative.Pastel  # Colores suaves
```

**Ajustar tamaño de fuente**:
Edita el CSS en `app.py` en la sección `st.markdown()`

## Análisis Paso a Paso

### Ejemplo Completo: Análisis de Satisfacción

**Escenario**: Tienes datos de satisfacción de clientes y quieres saber qué la afecta

**Datos necesarios**:
```csv
satisfaccion,edad,tiempo_espera,precio_percibido,categoria
4,45,10,3,Medicamentos
5,32,5,4,Cosmetica
3,67,15,2,Medicamentos
...
```

**Análisis**:

1. **Exploración Inicial**
   - Cargar CSV
   - Ver estadísticas descriptivas
   - Histograma de satisfacción

2. **Correlaciones**
   - Análisis → Correlaciones
   - Seleccionar: `satisfaccion`, `edad`, `tiempo_espera`, `precio_percibido`
   - Método: Pearson
   - **Resultado**: Matriz de correlación mostrando relaciones

3. **Comparación por Categoría**
   - Análisis → ANOVA
   - Variable dependiente: `satisfaccion`
   - Variable grupo: `categoria`
   - **Resultado**: ¿Hay diferencias significativas entre categorías?

4. **Modelo Predictivo**
   - Modelos → Regresión
   - Objetivo: `satisfaccion`
   - Predictoras: `edad`, `tiempo_espera`, `precio_percibido`
   - **Resultado**: Modelo que predice satisfacción + importancia de cada factor

5. **Interpretación IA**
   - Asistente IA → "Basándote en estos análisis, ¿qué factores debo mejorar para aumentar la satisfacción?"
   - **Resultado**: Recomendaciones prácticas

## Glosario Rápido

| Término | Significado |
|---------|-------------|
| **p-valor** | Probabilidad de error. Si < 0.05, el resultado es significativo |
| **R²** | % de varianza explicada por el modelo. Más alto = mejor |
| **Correlación** | Relación entre variables. -1 a 1 (0 = sin relación) |
| **ANOVA** | Compara medias de 3+ grupos |
| **Regresión** | Predice valores numéricos |
| **Clustering** | Agrupa datos similares |

## Recursos

- 📖 [Manual completo](../README.md)
- 🎥 [Video tutoriales](https://youtube.com/...)
- 💬 [Foro de ayuda](https://github.com/tu-usuario/data_fh/discussions)
- 🐛 [Reportar problema](https://github.com/tu-usuario/data_fh/issues)

---

**¿Dudas?** Usa el asistente IA dentro de la aplicación o consulta la documentación completa.
