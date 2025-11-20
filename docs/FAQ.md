# ❓ Preguntas Frecuentes (FAQ)

## General

### ¿Qué es este sistema?
Es una aplicación web local para análisis estadístico de datos farmacéuticos. Permite cargar datos (CSV/Excel), realizar análisis estadísticos avanzados, crear modelos predictivos y obtener asistencia de IA generativa, todo ejecutándose 100% en tu equipo.

### ¿Es gratis?
Sí, es completamente gratuito y de código abierto bajo licencia MIT.

### ¿Necesito conexión a internet?
No para el funcionamiento principal. Solo necesitas internet para:
- Instalar dependencias (primera vez)
- Descargar modelos de Ollama (primera vez)
- Acceder a la documentación online (opcional)

## Seguridad y RGPD

### ¿Es seguro para datos sensibles?
Sí, todos los datos se procesan localmente en tu equipo. No se envía nada a servidores externos.

### ¿Cumple con RGPD?
Sí, cumple totalmente con RGPD porque:
- Procesamiento 100% local
- No hay transmisión de datos a terceros
- Auto-eliminación de archivos temporales
- No se almacenan datos personales
- El usuario tiene control total sobre sus datos

### ¿Puedo usar datos de pacientes?
Sí, pero recomendamos:
- Anonimizar datos personales antes de cargarlos
- Usar códigos en lugar de nombres
- Eliminar información identificable
- Seguir las políticas de tu organización

### ¿Los datos se guardan en algún lugar?
Los archivos subidos se almacenan temporalmente en `data/uploads/` y se eliminan automáticamente al cerrar la sesión. Puedes configurar eliminación inmediata en `.env`.

## Instalación

### ¿Qué sistema operativo necesito?
Compatible con:
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu, Debian, Fedora, etc.)

### ¿Qué requisitos técnicos tiene?
Mínimos:
- Python 3.8+
- 4GB RAM
- 2GB espacio en disco

Recomendados:
- Python 3.10+
- 8GB RAM
- 5GB espacio (para modelos de IA)

### Error: "Python no encontrado"
**Solución**:
1. Instala Python desde https://www.python.org/downloads/
2. En Windows, marca "Add Python to PATH" durante instalación
3. Verifica: `python --version` o `python3 --version`

### Error al instalar dependencias
**Solución**:
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar con verbose para ver errores
pip install -r requirements.txt -v

# Si falla, instalar individualmente
pip install streamlit pandas numpy scipy scikit-learn plotly
```

## Uso de la Aplicación

### ¿Qué formatos de archivo acepta?
- CSV (.csv)
- Excel (.xlsx, .xls)

Asegúrate de que:
- La primera fila contenga nombres de columnas
- No haya caracteres especiales en nombres de columnas
- El archivo no esté corrupto

### ¿Cuál es el tamaño máximo de archivo?
Por defecto 100MB. Puedes cambiarlo en `.env`:
```
MAX_FILE_SIZE_MB=200
```

### Los gráficos no se muestran
**Soluciones**:
1. Refresca el navegador (F5)
2. Limpia la caché de Streamlit (presiona 'C')
3. Reinstala Plotly: `pip install --upgrade plotly`
4. Verifica que JavaScript esté habilitado en tu navegador

### ¿Puedo usar varios archivos a la vez?
Actualmente solo un archivo por sesión. Para combinar datos:
1. Usa Excel/Python para unir archivos
2. O carga uno, exporta resultados, carga otro

## Asistente IA

### ¿Qué es Ollama?
Es un software que ejecuta modelos de IA grandes (LLMs) localmente en tu computadora, sin necesidad de internet o servicios cloud.

### ¿Es necesario el asistente IA?
No, es opcional. Puedes usar todas las funciones de análisis sin IA. El asistente solo añade:
- Interpretaciones automáticas
- Sugerencias de análisis
- Explicaciones de conceptos

### Error: "Ollama no disponible"
**Solución**:
1. Instala Ollama: https://ollama.ai/download
2. Ejecuta: `ollama pull mistral`
3. Verifica que esté corriendo: `ollama list`
4. Reinicia la aplicación

### ¿Qué modelo de IA usar?
Recomendado: **Mistral** (balance rendimiento/tamaño)

Alternativas:
- `llama2`: Más ligero (7GB RAM)
- `mixtral`: Más potente (16GB RAM)
- `phi`: Muy ligero (4GB RAM)

Cambiar en `.env`:
```
OLLAMA_MODEL=llama2
```

### ¿La IA puede cometer errores?
Sí, como cualquier herramienta de IA. Usa el asistente como guía, pero:
- Verifica resultados importantes
- Contrasta con tu conocimiento del dominio
- No tomes decisiones críticas solo basándote en la IA

## Análisis Estadísticos

### ¿Qué análisis puedo hacer?
- Estadísticas descriptivas
- Correlaciones (Pearson, Spearman, Kendall)
- Prueba t de Student
- ANOVA
- Chi-cuadrado
- Regresión lineal múltiple
- Clustering (K-means)
- PCA
- Random Forest (regresión/clasificación)

### ¿Cuántos datos necesito?
Depende del análisis:
- Descriptivas: 10+ filas
- Correlaciones: 30+ filas
- Regresión: 50+ filas
- Machine Learning: 100+ filas (idealmente 500+)

### "No hay datos suficientes"
Tu dataset es muy pequeño para el análisis elegido. Opciones:
- Recolecta más datos
- Usa análisis más simples
- Combina datasets

### ¿Qué significa p-valor?
El p-valor indica la probabilidad de obtener estos resultados por azar:
- p < 0.05: Resultado significativo (95% confianza)
- p < 0.01: Muy significativo (99% confianza)
- p > 0.05: No significativo

**Ejemplo**: Si comparas ventas entre dos grupos y p=0.03, hay 97% de probabilidad de que la diferencia sea real, no casualidad.

### ¿Cómo interpreto R²?
R² indica qué % de la varianza explica tu modelo:
- R² = 0.90: Excelente (90% explicado)
- R² = 0.70: Bueno (70% explicado)
- R² = 0.50: Regular (50% explicado)
- R² = 0.30: Débil (30% explicado)

### ¿Correlación implica causalidad?
**NO**. Que dos variables estén correlacionadas no significa que una cause la otra.

Ejemplo: Ventas de helado y ahogamientos están correlacionados (ambos aumentan en verano), pero uno no causa el otro.

## Modelos Predictivos

### ¿Qué es Random Forest?
Un algoritmo de machine learning que:
- Crea múltiples árboles de decisión
- Combina sus predicciones
- Es robusto y fácil de usar
- Maneja bien datos complejos

### ¿Cómo sé si mi modelo es bueno?
Para **regresión**:
- R² > 0.70: Bueno
- RMSE bajo comparado con el rango de datos

Para **clasificación**:
- Accuracy > 0.80: Bueno
- Depende del contexto

### Mi modelo tiene baja precisión
Posibles causas:
- Pocas muestras de entrenamiento
- Variables no relevantes
- Relación no lineal compleja
- Datos con mucho ruido

Soluciones:
- Más datos
- Mejores features
- Feature engineering
- Probar otros algoritmos

## Visualizaciones

### ¿Puedo descargar los gráficos?
Sí, pasa el cursor sobre el gráfico y haz clic en el icono de cámara (📷) en la esquina superior derecha.

### ¿Puedo personalizar colores?
Sí, edita `modules/visualizations.py`:
```python
self.color_palette = px.colors.qualitative.Pastel
```

Opciones: `Set1`, `Set2`, `Set3`, `Pastel`, `Dark24`, etc.

### Los gráficos se ven mal en pantalla pequeña
Ajusta el zoom del navegador (Ctrl +/-) o usa el modo amplio de Streamlit (presiona 'W').

## Exportación

### ¿En qué formatos puedo exportar?
- CSV (datos y estadísticas)
- Excel (datos)
- PNG (gráficos, manualmente)

### ¿Puedo generar reportes automáticos?
Actualmente no, pero está en el roadmap. Por ahora:
1. Exporta resultados a Excel
2. Descarga gráficos como PNG
3. Crea tu reporte manualmente

## Problemas Técnicos

### La aplicación no inicia
```bash
# Verifica que el entorno virtual esté activo
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstala dependencias
pip install -r requirements.txt

# Ejecuta con verbose
streamlit run app.py --logger.level=debug
```

### Error: "Address already in use"
Otro proceso usa el puerto 8501. Soluciones:
```bash
# Opción 1: Usa otro puerto
streamlit run app.py --server.port 8502

# Opción 2: Mata el proceso anterior
# Linux/Mac:
lsof -ti:8501 | xargs kill -9

# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### La aplicación es lenta
Posibles causas:
- Archivo muy grande: Reduce el dataset
- Análisis complejo: Reduce variables
- Poca RAM: Cierra otros programas
- Ollama consumiendo recursos: Usa modelo más ligero

### Error: "Memory error"
Tu dataset es muy grande. Soluciones:
1. Muestrea tu dataset (toma una muestra aleatoria)
2. Aumenta RAM del sistema
3. Procesa en lotes más pequeños

## Desarrollo y Contribuciones

### ¿Puedo modificar el código?
Sí, el proyecto es open source (Licencia MIT). Puedes:
- Modificar para tus necesidades
- Añadir funcionalidades
- Hacer fork del proyecto
- Contribuir con pull requests

### ¿Cómo reporto un bug?
1. Ve a https://github.com/tu-usuario/data_fh/issues
2. Haz clic en "New Issue"
3. Describe el problema con detalles:
   - Qué intentabas hacer
   - Qué sucedió
   - Mensajes de error
   - Sistema operativo y versión de Python

### ¿Puedo solicitar funcionalidades?
Sí, abre un "Feature Request" en GitHub Issues describiendo:
- Qué funcionalidad necesitas
- Por qué sería útil
- Casos de uso

## Mejores Prácticas

### Preparación de datos
1. Limpia datos antes de cargar
2. Usa nombres de columnas descriptivos sin espacios
3. Verifica tipos de datos (números como números, no texto)
4. Elimina filas completamente vacías

### Flujo de trabajo recomendado
1. **Exploración**: Conoce tus datos
2. **Limpieza**: Maneja valores nulos
3. **Visualización**: Identifica patrones
4. **Análisis**: Pruebas estadísticas
5. **Modelado**: Si buscas predicción
6. **Interpretación**: Usa IA para entender
7. **Exportación**: Guarda resultados

### Seguridad
- No compartas archivos .env
- Anonimiza datos sensibles
- Usa en red privada
- Haz backups regularmente

---

## Más Ayuda

¿No encuentras tu pregunta?

- 📖 [Documentación completa](../README.md)
- 💬 [Foro de discusiones](https://github.com/tu-usuario/data_fh/discussions)
- 🐛 [Reportar problema](https://github.com/tu-usuario/data_fh/issues)
- 🤖 Pregunta al asistente IA dentro de la app

---

*Última actualización: 2024*
