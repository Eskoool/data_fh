/**
 * Aplicación principal - Manejo de UI y eventos
 */

// Variables globales
let analyzer = new DataAnalyzer();
let currentFileName = '';

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupFileUpload();
    setupDragAndDrop();
    console.log('📊 Aplicación de Análisis Farmacéutico iniciada');
}

/**
 * Configurar carga de archivos
 */
function setupFileUpload() {
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', handleFileSelect);
}

/**
 * Configurar drag and drop
 */
function setupDragAndDrop() {
    const uploadArea = document.getElementById('uploadArea');

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    uploadArea.addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
}

/**
 * Maneja la selección de archivo
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        handleFile(file);
    }
}

/**
 * Procesa el archivo CSV
 */
function handleFile(file) {
    if (!file.name.endsWith('.csv')) {
        alert('⚠️ Por favor selecciona un archivo CSV');
        return;
    }

    currentFileName = file.name;

    Papa.parse(file, {
        header: true,
        dynamicTyping: false,
        skipEmptyLines: true,
        complete: function(results) {
            if (results.errors.length > 0) {
                console.error('Errores al parsear CSV:', results.errors);
                alert('⚠️ Error al leer el archivo. Verifica que sea un CSV válido.');
                return;
            }

            analyzer.loadData(results);
            displayData();
            showAlert('✅ Datos cargados correctamente', 'success');
        },
        error: function(error) {
            console.error('Error:', error);
            alert('❌ Error al cargar el archivo');
        }
    });
}

/**
 * Muestra los datos cargados
 */
function displayData() {
    const summary = analyzer.getSummary();

    // Actualizar información
    document.getElementById('rowCount').textContent = summary.rows.toLocaleString();
    document.getElementById('colCount').textContent = summary.columns;
    document.getElementById('fileName').textContent = currentFileName;

    // Mostrar tabla (primeras 100 filas)
    displayTable(analyzer.data.slice(0, 100), analyzer.headers);

    // Poblar selectores
    populateSelectors();

    // Mostrar secciones
    document.getElementById('preview-section').style.display = 'block';
    document.getElementById('analysis-section').style.display = 'block';
    document.getElementById('export-section').style.display = 'block';

    // Scroll suave
    document.getElementById('preview-section').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Muestra la tabla de datos
 */
function displayTable(data, headers) {
    const thead = document.getElementById('tableHead');
    const tbody = document.getElementById('tableBody');

    // Limpiar
    thead.innerHTML = '';
    tbody.innerHTML = '';

    // Headers
    const headerRow = document.createElement('tr');
    headers.forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Datos
    data.forEach(row => {
        const tr = document.createElement('tr');
        headers.forEach(header => {
            const td = document.createElement('td');
            td.textContent = row[header] || '-';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

/**
 * Pobla todos los selectores con las columnas
 */
function populateSelectors() {
    const selectors = ['statsVariable', 'vizVariable', 'vizVariable2'];

    selectors.forEach(selectorId => {
        const select = document.getElementById(selectorId);
        select.innerHTML = '<option value="">-- Seleccionar --</option>';

        analyzer.headers.forEach(header => {
            const option = document.createElement('option');
            option.value = header;
            option.textContent = header;
            select.appendChild(option);
        });
    });
}

/**
 * Cambia de pestaña
 */
function switchTab(tabName) {
    // Ocultar todas las pestañas
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remover active de botones
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Activar pestaña seleccionada
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // Activar botón
    event.target.classList.add('active');
}

/**
 * Calcula estadísticas descriptivas
 */
function calculateStatistics() {
    const variable = document.getElementById('statsVariable').value;
    if (!variable) return;

    const stats = analyzer.calculateStats(variable);
    const resultsDiv = document.getElementById('statisticsResults');

    if (stats.type === 'categorical') {
        displayCategoricalStats(stats, variable, resultsDiv);
    } else {
        displayNumericStats(stats, variable, resultsDiv);
    }
}

/**
 * Muestra estadísticas numéricas
 */
function displayNumericStats(stats, variable, container) {
    const html = `
        <h3>📊 Estadísticas de: ${variable}</h3>
        <div class="stat-grid">
            <div class="stat-item">
                <span class="stat-label">Conteo</span>
                <span class="stat-value">${stats.count}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Media</span>
                <span class="stat-value">${stats.mean.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Mediana</span>
                <span class="stat-value">${stats.median.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Desv. Estándar</span>
                <span class="stat-value">${stats.std.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Mínimo</span>
                <span class="stat-value">${stats.min.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Máximo</span>
                <span class="stat-value">${stats.max.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Q1 (25%)</span>
                <span class="stat-value">${stats.q1.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Q3 (75%)</span>
                <span class="stat-value">${stats.q3.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Rango</span>
                <span class="stat-value">${stats.range.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">IQR</span>
                <span class="stat-value">${stats.iqr.toFixed(2)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Asimetría</span>
                <span class="stat-value">${stats.skewness.toFixed(3)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Curtosis</span>
                <span class="stat-value">${stats.kurtosis.toFixed(3)}</span>
            </div>
        </div>

        <div class="mt-2">
            <h4>📌 Interpretación</h4>
            <p><strong>Coeficiente de Variación:</strong> ${stats.cv.toFixed(2)}% ${stats.cv > 30 ? '(Alta variabilidad)' : '(Baja variabilidad)'}</p>
            <p><strong>Distribución:</strong> ${Math.abs(stats.skewness) < 0.5 ? 'Simétrica' : (stats.skewness > 0 ? 'Asimétrica positiva (cola derecha)' : 'Asimétrica negativa (cola izquierda)')}</p>
        </div>
    `;

    container.innerHTML = html;

    // Test de normalidad
    const normalityTest = analyzer.testNormality(variable);
    const normalityHtml = `
        <div class="mt-2 alert ${normalityTest.isNormal ? 'alert-success' : 'alert-warning'}">
            <h4>🔬 Test de Normalidad</h4>
            <p>${normalityTest.interpretation}</p>
            <p><em>${normalityTest.recommendation}</em></p>
        </div>
    `;
    container.innerHTML += normalityHtml;

    // Outliers
    const outliers = analyzer.findOutliers(variable);
    if (outliers.count > 0) {
        const outliersHtml = `
            <div class="mt-2 alert alert-warning">
                <h4>⚠️ Valores Atípicos (Outliers)</h4>
                <p>Se detectaron <strong>${outliers.count}</strong> valores atípicos (${outliers.percentage}% de los datos)</p>
                <p>Rango normal: ${outliers.lowerBound.toFixed(2)} - ${outliers.upperBound.toFixed(2)}</p>
            </div>
        `;
        container.innerHTML += outliersHtml;
    }
}

/**
 * Muestra estadísticas categóricas
 */
function displayCategoricalStats(stats, variable, container) {
    let tableHtml = `
        <h3>📊 Frecuencias de: ${variable}</h3>
        <p>Valores únicos: <strong>${stats.unique}</strong></p>
        <p>Moda: <strong>${stats.mode}</strong> (${stats.modeCount} veces)</p>

        <table class="mt-2">
            <thead>
                <tr>
                    <th>Valor</th>
                    <th>Frecuencia</th>
                    <th>Porcentaje</th>
                    <th>Acumulado</th>
                </tr>
            </thead>
            <tbody>
    `;

    stats.frequencyTable.forEach(row => {
        tableHtml += `
            <tr>
                <td>${row.value}</td>
                <td>${row.count}</td>
                <td>${row.percentage}%</td>
                <td>${row.cumulative}%</td>
            </tr>
        `;
    });

    tableHtml += '</tbody></table>';
    container.innerHTML = tableHtml;
}

/**
 * Actualiza opciones de gráfico según el tipo seleccionado
 */
function updateChartOptions() {
    const chartType = document.getElementById('chartType').value;
    const viz2Group = document.getElementById('vizVariable2Group');

    if (chartType === 'scatter') {
        viz2Group.style.display = 'block';
    } else {
        viz2Group.style.display = 'none';
    }
}

/**
 * Crea visualización
 */
function createVisualization() {
    const chartType = document.getElementById('chartType').value;
    const variable1 = document.getElementById('vizVariable').value;
    const variable2 = document.getElementById('vizVariable2').value;

    if (!variable1) {
        alert('Selecciona una variable');
        return;
    }

    const ctx = document.getElementById('mainChart').getContext('2d');

    // Destruir gráfico anterior
    if (analyzer.currentChart) {
        analyzer.currentChart.destroy();
    }

    let chartData, chartConfig;

    switch (chartType) {
        case 'histogram':
            chartData = analyzer.prepareHistogramData(variable1);
            chartConfig = {
                type: 'bar',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: variable1,
                        data: chartData.data,
                        backgroundColor: 'rgba(31, 119, 180, 0.7)',
                        borderColor: 'rgba(31, 119, 180, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        title: {
                            display: true,
                            text: `Histograma de ${variable1}`
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Frecuencia'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: variable1
                            }
                        }
                    }
                }
            };
            break;

        case 'bar':
            chartData = analyzer.prepareBarChartData(variable1);
            chartConfig = {
                type: 'bar',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: variable1,
                        data: chartData.data,
                        backgroundColor: 'rgba(255, 127, 14, 0.7)',
                        borderColor: 'rgba(255, 127, 14, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: `Frecuencias de ${variable1}`
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Frecuencia'
                            }
                        }
                    }
                }
            };
            break;

        case 'line':
            chartData = analyzer.prepareLineChartData(variable1, variable1);
            chartConfig = {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: variable1,
                        data: chartData.data,
                        borderColor: 'rgba(44, 160, 44, 1)',
                        backgroundColor: 'rgba(44, 160, 44, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: `Evolución de ${variable1}`
                        }
                    }
                }
            };
            break;

        case 'scatter':
            if (!variable2) {
                alert('Selecciona la variable Y para el gráfico de dispersión');
                return;
            }
            chartData = analyzer.prepareScatterData(variable1, variable2);
            chartConfig = {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: `${variable1} vs ${variable2}`,
                        data: chartData,
                        backgroundColor: 'rgba(214, 39, 40, 0.6)',
                        borderColor: 'rgba(214, 39, 40, 1)'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: `Dispersión: ${variable1} vs ${variable2}`
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: variable1
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: variable2
                            }
                        }
                    }
                }
            };
            break;

        case 'pie':
            chartData = analyzer.prepareBarChartData(variable1, 5);
            chartConfig = {
                type: 'pie',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        data: chartData.data,
                        backgroundColor: [
                            'rgba(31, 119, 180, 0.7)',
                            'rgba(255, 127, 14, 0.7)',
                            'rgba(44, 160, 44, 0.7)',
                            'rgba(214, 39, 40, 0.7)',
                            'rgba(148, 103, 189, 0.7)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: `Distribución de ${variable1}`
                        }
                    }
                }
            };
            break;
    }

    analyzer.currentChart = new Chart(ctx, chartConfig);
}

/**
 * Calcula y muestra matriz de correlación
 */
function calculateCorrelations() {
    const corrData = analyzer.calculateCorrelationMatrix();

    if (!corrData) {
        alert('Se necesitan al menos 2 variables numéricas');
        return;
    }

    displayCorrelationMatrix(corrData);
    createCorrelationHeatmap(corrData);
}

/**
 * Muestra matriz de correlación como tabla
 */
function displayCorrelationMatrix(corrData) {
    const container = document.getElementById('correlationResults');

    let html = `
        <h3>Matriz de Correlación de Pearson</h3>
        <div class="correlation-matrix">
            <table>
                <thead>
                    <tr>
                        <th></th>
    `;

    corrData.columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';

    corrData.matrix.forEach((row, i) => {
        html += `<tr><th>${corrData.columns[i]}</th>`;
        row.forEach(val => {
            const absVal = Math.abs(val);
            let colorClass = 'correlation-low';
            if (absVal > 0.7) colorClass = 'correlation-high';
            else if (absVal > 0.4) colorClass = 'correlation-medium';

            html += `<td class="correlation-cell ${colorClass}">${val.toFixed(3)}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table></div>';

    html += `
        <div class="mt-2">
            <p><strong>Interpretación:</strong></p>
            <ul>
                <li>Valores cercanos a 1 o -1: Correlación fuerte</li>
                <li>Valores cercanos a 0: Sin correlación</li>
                <li>Positivos: Relación directa | Negativos: Relación inversa</li>
            </ul>
        </div>
    `;

    container.innerHTML = html;
}

/**
 * Crea mapa de calor de correlaciones
 */
function createCorrelationHeatmap(corrData) {
    // Implementación simplificada - Chart.js no tiene heatmap nativo
    // Aquí podrías usar una librería como Plotly.js para un verdadero heatmap
    console.log('Matriz de correlación:', corrData);
}

/**
 * Actualiza opciones de prueba estadística
 */
function updateTestOptions() {
    const testType = document.getElementById('testType').value;
    const controlsDiv = document.getElementById('testControls');
    const resultsDiv = document.getElementById('testResults');

    resultsDiv.innerHTML = '';

    if (!testType) {
        controlsDiv.innerHTML = '';
        return;
    }

    let html = '';

    if (testType === 'ttest') {
        html = `
            <div class="controls-row">
                <div class="control-group">
                    <label for="ttestNumeric">Variable Numérica:</label>
                    <select id="ttestNumeric">
                        ${analyzer.numericColumns.map(col => `<option value="${col}">${col}</option>`).join('')}
                    </select>
                </div>
                <div class="control-group">
                    <label for="ttestCategorical">Variable Categórica (2 grupos):</label>
                    <select id="ttestCategorical">
                        ${analyzer.categoricalColumns.map(col => `<option value="${col}">${col}</option>`).join('')}
                    </select>
                </div>
                <button class="btn btn-primary" onclick="performTTest()">Ejecutar Prueba t</button>
            </div>
        `;
    } else if (testType === 'normality') {
        html = `
            <div class="controls-row">
                <div class="control-group">
                    <label for="normalityVariable">Variable:</label>
                    <select id="normalityVariable">
                        ${analyzer.numericColumns.map(col => `<option value="${col}">${col}</option>`).join('')}
                    </select>
                </div>
                <button class="btn btn-primary" onclick="performNormalityTest()">Ejecutar Test</button>
            </div>
        `;
    } else if (testType === 'comparison') {
        html = `
            <div class="controls-row">
                <div class="control-group">
                    <label for="compVariable">Variable a comparar:</label>
                    <select id="compVariable">
                        ${analyzer.numericColumns.map(col => `<option value="${col}">${col}</option>`).join('')}
                    </select>
                </div>
                <div class="control-group">
                    <label for="groupVariable">Agrupar por:</label>
                    <select id="groupVariable">
                        ${analyzer.categoricalColumns.map(col => `<option value="${col}">${col}</option>`).join('')}
                    </select>
                </div>
                <button class="btn btn-primary" onclick="performGroupComparison()">Comparar</button>
            </div>
        `;
    }

    controlsDiv.innerHTML = html;
}

/**
 * Realiza prueba t
 */
function performTTest() {
    const numericVar = document.getElementById('ttestNumeric').value;
    const categoricalVar = document.getElementById('ttestCategorical').value;

    try {
        const result = analyzer.performTTest(numericVar, categoricalVar);
        const resultsDiv = document.getElementById('testResults');

        const html = `
            <div class="alert ${result.significant ? 'alert-success' : 'alert-info'}">
                <h3>📊 Resultados Prueba t de Student</h3>

                <div class="stat-grid">
                    <div class="stat-item">
                        <span class="stat-label">${result.group1Name} - Media</span>
                        <span class="stat-value">${result.mean1.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">${result.group2Name} - Media</span>
                        <span class="stat-value">${result.mean2.toFixed(2)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Estadístico t</span>
                        <span class="stat-value">${result.t.toFixed(3)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Grados de libertad</span>
                        <span class="stat-value">${result.df}</span>
                    </div>
                </div>

                <div class="mt-2">
                    <p><strong>Interpretación:</strong> ${result.interpretation}</p>
                    <p><strong>Tamaño del efecto (d de Cohen):</strong> ${result.cohensD.toFixed(3)} (${result.effectSize})</p>
                </div>
            </div>
        `;

        resultsDiv.innerHTML = html;
    } catch (error) {
        alert(error.message);
    }
}

/**
 * Realiza test de normalidad
 */
function performNormalityTest() {
    const variable = document.getElementById('normalityVariable').value;
    const result = analyzer.testNormality(variable);
    const resultsDiv = document.getElementById('testResults');

    const html = `
        <div class="alert ${result.isNormal ? 'alert-success' : 'alert-warning'}">
            <h3>🔬 Test de Normalidad</h3>
            <p><strong>${result.interpretation}</strong></p>
            <div class="mt-2">
                <p>Asimetría: ${result.skewness.toFixed(3)}</p>
                <p>Curtosis: ${result.kurtosis.toFixed(3)}</p>
            </div>
            <p class="mt-2"><em>${result.recommendation}</em></p>
        </div>
    `;

    resultsDiv.innerHTML = html;
}

/**
 * Compara medias por grupos
 */
function performGroupComparison() {
    const variable = document.getElementById('compVariable').value;
    const groupVar = document.getElementById('groupVariable').value;

    const groups = {};
    analyzer.data.forEach(row => {
        const group = row[groupVar];
        const value = parseFloat(row[variable]);

        if (!isNaN(value)) {
            if (!groups[group]) groups[group] = [];
            groups[group].push(value);
        }
    });

    let html = '<h3>📊 Comparación de Medias por Grupo</h3><div class="stat-grid">';

    Object.entries(groups).forEach(([group, values]) => {
        const mean = ss.mean(values);
        const std = ss.standardDeviation(values);

        html += `
            <div class="stat-item">
                <span class="stat-label">${group}</span>
                <span class="stat-value">${mean.toFixed(2)} ± ${std.toFixed(2)}</span>
            </div>
        `;
    });

    html += '</div>';

    document.getElementById('testResults').innerHTML = html;
}

/**
 * Exporta datos a CSV
 */
function exportToCSV() {
    const csv = analyzer.exportToCSV();
    downloadFile(csv, 'datos_farmacia.csv', 'text/csv');
    showAlert('✅ Datos exportados', 'success');
}

/**
 * Exporta estadísticas
 */
function exportStatistics() {
    const csv = analyzer.exportStatistics();
    downloadFile(csv, 'estadisticas_farmacia.csv', 'text/csv');
    showAlert('✅ Estadísticas exportadas', 'success');
}

/**
 * Exporta gráfico como imagen
 */
function exportChart() {
    if (!analyzer.currentChart) {
        alert('Primero genera un gráfico');
        return;
    }

    const canvas = document.getElementById('mainChart');
    const url = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = 'grafico_farmacia.png';
    link.href = url;
    link.click();

    showAlert('✅ Gráfico exportado', 'success');
}

/**
 * Descarga un archivo
 */
function downloadFile(content, fileName, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    link.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Muestra alerta
 */
function showAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';

    document.body.appendChild(alert);

    setTimeout(() => {
        alert.remove();
    }, 3000);
}

/**
 * Limpia los datos
 */
function clearData() {
    if (confirm('¿Seguro que quieres limpiar todos los datos?')) {
        analyzer = new DataAnalyzer();
        currentFileName = '';

        document.getElementById('preview-section').style.display = 'none';
        document.getElementById('analysis-section').style.display = 'none';
        document.getElementById('export-section').style.display = 'none';

        showAlert('🗑️ Datos eliminados', 'info');
    }
}

/**
 * Carga datos de ejemplo
 */
function loadExampleData() {
    // Datos de ejemplo de farmacia
    const exampleCSV = `fecha,ventas_euros,num_clientes,categoria,prescripcion,satisfaccion,edad_promedio,temperatura
2023-01-01,2156.32,45,Medicamentos,Si,4,42.3,18.5
2023-01-02,1987.54,52,Cosmetica,No,5,35.2,19.1
2023-01-03,2345.67,48,Higiene,No,3,51.4,17.8
2023-01-04,1876.23,41,Nutricion,No,4,39.7,20.2
2023-01-05,2543.12,55,Medicamentos,Si,5,48.9,21.3
2023-01-06,1654.89,38,Medicamentos,Si,3,62.1,19.7
2023-01-07,2234.56,49,Cosmetica,No,4,33.8,18.9
2023-01-08,2012.34,46,Higiene,No,5,44.6,22.1
2023-01-09,2456.78,53,Medicamentos,Si,4,56.3,20.8
2023-01-10,1789.45,42,Nutricion,No,3,41.2,19.3`;

    currentFileName = 'datos_ejemplo.csv';

    Papa.parse(exampleCSV, {
        header: true,
        dynamicTyping: false,
        skipEmptyLines: true,
        complete: function(results) {
            analyzer.loadData(results);
            displayData();
            showAlert('✅ Datos de ejemplo cargados', 'success');
        }
    });
}
