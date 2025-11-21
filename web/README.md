# 🌐 Versión HTML Standalone

**Análisis de Datos Farmacéuticos - Sin instalación**

## 🚀 Inicio Rápido (30 segundos)

1. **Abre** el archivo `index.html` en tu navegador
2. **Arrastra** tu archivo CSV o usa datos de ejemplo
3. **¡Listo!** Comienza a analizar

No se requiere instalación de Python, Node.js ni ningún software adicional.

---

## ✨ Características

### 📊 Análisis Disponibles

- ✅ **Estadísticas Descriptivas**
  - Media, mediana, desviación estándar
  - Cuartiles, rango, IQR
  - Asimetría y curtosis
  - Coeficiente de variación

- ✅ **Visualizaciones Interactivas**
  - Histogramas
  - Gráficos de barras
  - Dispersión (scatter plot)
  - Líneas temporales
  - Gráficos circulares

- ✅ **Correlaciones**
  - Matriz de correlación de Pearson
  - Visualización con colores

- ✅ **Pruebas Estadísticas**
  - Prueba t de Student (2 grupos)
  - Test de normalidad
  - Comparación de medias por grupos
  - Detección de outliers

- ✅ **Exportación**
  - Descargar datos en CSV
  - Exportar estadísticas
  - Guardar gráficos como PNG

### 🔒 Privacidad Total

- **100% Local**: Todo se ejecuta en tu navegador
- **Sin servidores**: No se envía nada a internet
- **Sin cookies**: No se rastrea tu actividad
- **RGPD compliant**: Cumplimiento total

---

## 📁 Estructura de Archivos

```
web/
├── index.html           # Aplicación principal
├── css/
│   └── style.css       # Estilos minimalistas
└── js/
    ├── app.js          # Lógica de la aplicación
    ├── analyzer.js     # Análisis de datos
    └── stats.js        # Funciones estadísticas
```

---

## 🎯 Cómo Usar

### 1️⃣ Cargar Datos

**Opción A: Drag & Drop**
- Arrastra tu archivo CSV a la zona de carga

**Opción B: Seleccionar archivo**
- Haz clic en "Seleccionar Archivo CSV"
- Navega y selecciona tu archivo

**Opción C: Datos de ejemplo**
- Haz clic en "Usar Datos de Ejemplo"
- Se cargan datos de farmacia sintéticos

### 2️⃣ Explorar Datos

- **Vista previa**: Tabla con las primeras 100 filas
- **Información**: Número de filas, columnas, nombre del archivo
- Los datos se mantienen en memoria mientras uses la aplicación

### 3️⃣ Analizar

#### 📊 Estadísticas
1. Ve a la pestaña "Estadísticas"
2. Selecciona una variable
3. Visualiza estadísticas completas

#### 📈 Visualizaciones
1. Pestaña "Visualizaciones"
2. Elige tipo de gráfico
3. Selecciona variable(s)
4. Genera el gráfico

#### 🔗 Correlaciones
1. Pestaña "Correlaciones"
2. Haz clic en "Calcular Correlaciones"
3. Visualiza la matriz coloreada

#### 🧪 Pruebas Estadísticas
1. Pestaña "Pruebas Estadísticas"
2. Selecciona el tipo de prueba
3. Configura variables
4. Ejecuta la prueba

### 4️⃣ Exportar

- **CSV**: Descarga los datos originales
- **Estadísticas**: Exporta resumen en CSV
- **Gráfico**: Guarda como imagen PNG

---

## 📋 Requisitos del Archivo CSV

### Formato Correcto

```csv
variable1,variable2,variable3
10,valor1,2023-01-01
20,valor2,2023-01-02
30,valor3,2023-01-03
```

### Reglas

1. ✅ Primera fila = nombres de columnas
2. ✅ Separador: coma (`,`)
3. ✅ Codificación: UTF-8
4. ✅ Sin filas completamente vacías

### Errores Comunes

❌ **Punto y coma (`;`) como separador**
- Solución: Usa Excel → Guardar como CSV (delimitado por comas)

❌ **Columnas sin nombre**
- Solución: Añade encabezados en la primera fila

❌ **Caracteres extraños**
- Solución: Guarda el archivo con codificación UTF-8

---

## 🎓 Ejemplos de Uso

### Caso 1: Análisis de Ventas

**Objetivo**: ¿Las ventas están correlacionadas con el número de clientes?

1. Carga tu CSV con columnas: `ventas`, `num_clientes`
2. Pestaña "Correlaciones" → Calcular
3. Busca el valor de correlación entre ambas
4. **Interpretación**:
   - r > 0.7: Correlación fuerte positiva
   - r < -0.7: Correlación fuerte negativa
   - |r| < 0.3: Sin correlación

### Caso 2: Comparar Medicamentos

**Objetivo**: ¿Hay diferencia en ventas entre medicamentos con/sin prescripción?

1. Datos con: `ventas`, `prescripcion` (Si/No)
2. Pruebas Estadísticas → Prueba t
3. Variable numérica: `ventas`
4. Variable categórica: `prescripcion`
5. **Resultado**: Te dirá si la diferencia es significativa

### Caso 3: Distribución de Edades

**Objetivo**: Ver la distribución de edades de clientes

1. Visualizaciones → Histograma
2. Variable: `edad`
3. Genera gráfico
4. **Análisis**: Observa si es simétrica, sesgada, etc.

---

## 🔧 Bibliotecas Utilizadas (CDN)

Esta versión usa bibliotecas JavaScript desde CDN:

- **[Chart.js](https://www.chartjs.org/)** v4.4.0 - Gráficos interactivos
- **[PapaParse](https://www.papaparse.com/)** v5.4.1 - Parser de CSV
- **[simple-statistics](https://simplestatistics.org/)** v7.8.3 - Funciones estadísticas

**¿Funciona sin internet?**
- Sí, si las bibliotecas están cacheadas
- Para uso 100% offline, descarga las librerías localmente

---

## 🆚 Comparación con Versión Streamlit

| Característica | HTML (esta) | Streamlit |
|----------------|-------------|-----------|
| **Instalación** | ❌ No requiere | ✅ Requiere Python |
| **Portabilidad** | ✅ Cualquier navegador | ⚠️ Requiere ejecutar servidor |
| **Análisis básicos** | ✅ | ✅ |
| **Análisis avanzados** | ⚠️ Limitados | ✅ Completos |
| **Machine Learning** | ❌ | ✅ Random Forest, PCA |
| **IA Generativa** | ❌ | ✅ Ollama local |
| **R Integration** | ❌ | ✅ Opcional |
| **Velocidad** | ✅ Instantánea | ⚠️ Requiere inicio |
| **Datasets grandes** | ⚠️ < 10,000 filas | ✅ Sin límite |

### ¿Cuándo usar cada versión?

**Usa HTML si:**
- No quieres instalar nada
- Análisis rápidos y simples
- Compartir con otros fácilmente
- Datasets pequeños (< 5,000 filas)

**Usa Streamlit si:**
- Necesitas análisis avanzados
- Machine Learning
- Asistente IA
- Datasets grandes
- Integración con R

---

## 🚀 Mejoras Futuras

### Próximas Funcionalidades

- [ ] ANOVA de un factor
- [ ] Regresión múltiple visualizada
- [ ] Heatmap de correlaciones mejorado
- [ ] Análisis de series temporales
- [ ] Prueba Chi-cuadrado
- [ ] Intervalos de confianza en gráficos
- [ ] Importar Excel directamente
- [ ] Exportar reportes en PDF

### Contribuciones

¿Quieres añadir funcionalidades?
1. Edita los archivos en `web/js/`
2. Prueba localmente
3. Envía un Pull Request

---

## 🆘 Solución de Problemas

### El archivo no se carga

**Causa**: Formato incorrecto de CSV

**Solución**:
1. Abre el CSV en un editor de texto
2. Verifica que la primera fila tenga nombres de columnas
3. Comprueba que use comas (`,`) como separador
4. Guarda con codificación UTF-8

### Los gráficos no aparecen

**Causa**: Bloqueador de JavaScript o problemas de CDN

**Solución**:
1. Verifica que JavaScript esté habilitado
2. Abre la consola del navegador (F12) y busca errores
3. Intenta con otro navegador
4. Comprueba conexión a internet (para CDN)

### "Error al calcular estadísticas"

**Causa**: Variable no numérica

**Solución**:
- Las estadísticas descriptivas solo funcionan con números
- Para variables categóricas usa tabla de frecuencias

### Rendimiento lento con muchos datos

**Causa**: El navegador tiene límites de memoria

**Solución**:
1. Reduce el tamaño del dataset (muestrea datos)
2. Usa la versión Streamlit para archivos grandes
3. Cierra otras pestañas del navegador

---

## 📞 Soporte

- 📖 [Documentación principal](../README.md)
- 💬 [GitHub Issues](https://github.com/Eskoool/data_fh/issues)
- 📧 Reporta bugs abriendo un issue

---

## 📄 Licencia

MIT License - Uso libre personal y comercial

---

## 🎉 ¡Disfruta Analizando!

Esta versión es perfecta para análisis rápidos sin complicaciones.
Para análisis más avanzados, prueba la [versión Streamlit completa](../README.md).

**Hecho con ❤️ para profesionales de farmacia**

*Versión HTML 1.0 | Última actualización: 2024*
