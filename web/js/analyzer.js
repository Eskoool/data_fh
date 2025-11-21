/**
 * Analizador de datos - Lógica de negocio
 */

class DataAnalyzer {
    constructor() {
        this.data = null;
        this.headers = null;
        this.numericColumns = [];
        this.categoricalColumns = [];
        this.currentChart = null;
    }

    /**
     * Carga datos desde CSV parseado
     */
    loadData(parsedData) {
        this.data = parsedData.data;
        this.headers = parsedData.meta.fields;
        this.identifyColumnTypes();
        return true;
    }

    /**
     * Identifica tipos de columnas (numérico vs categórico)
     */
    identifyColumnTypes() {
        this.numericColumns = [];
        this.categoricalColumns = [];

        this.headers.forEach(header => {
            const column = this.getColumn(header);
            const numericValues = column.filter(val => Stats.isNumeric(val));

            // Si más del 80% son numéricos, considerar como numérico
            if (numericValues.length / column.length > 0.8) {
                this.numericColumns.push(header);
            } else {
                this.categoricalColumns.push(header);
            }
        });
    }

    /**
     * Obtiene una columna como array
     */
    getColumn(columnName) {
        return this.data.map(row => row[columnName]).filter(val => val !== null && val !== '');
    }

    /**
     * Obtiene una columna numérica (parsea a float)
     */
    getNumericColumn(columnName) {
        return this.getColumn(columnName)
            .map(val => parseFloat(val))
            .filter(val => !isNaN(val));
    }

    /**
     * Calcula estadísticas descriptivas para una columna
     */
    calculateStats(columnName) {
        if (!this.numericColumns.includes(columnName)) {
            return this.calculateCategoricalStats(columnName);
        }

        const data = this.getNumericColumn(columnName);
        return Stats.descriptiveStats(data);
    }

    /**
     * Calcula estadísticas para variables categóricas
     */
    calculateCategoricalStats(columnName) {
        const data = this.getColumn(columnName);
        const freqTable = Stats.frequencyTable(data);

        return {
            type: 'categorical',
            count: data.length,
            unique: new Set(data).size,
            mode: freqTable[0].value,
            modeCount: freqTable[0].count,
            frequencyTable: freqTable
        };
    }

    /**
     * Calcula matriz de correlación
     */
    calculateCorrelationMatrix() {
        if (this.numericColumns.length < 2) {
            return null;
        }

        const dataMatrix = this.numericColumns.map(col => this.getNumericColumn(col));
        const corrMatrix = Stats.correlationMatrix(dataMatrix);

        return {
            columns: this.numericColumns,
            matrix: corrMatrix
        };
    }

    /**
     * Realiza prueba t de dos muestras
     */
    performTTest(numericColumn, categoricalColumn) {
        const categories = [...new Set(this.getColumn(categoricalColumn))];

        if (categories.length !== 2) {
            throw new Error('La variable categórica debe tener exactamente 2 grupos');
        }

        const group1Data = [];
        const group2Data = [];

        this.data.forEach(row => {
            const value = parseFloat(row[numericColumn]);
            if (!isNaN(value)) {
                if (row[categoricalColumn] === categories[0]) {
                    group1Data.push(value);
                } else if (row[categoricalColumn] === categories[1]) {
                    group2Data.push(value);
                }
            }
        });

        const result = Stats.tTestTwoSample(group1Data, group2Data);
        result.group1Name = categories[0];
        result.group2Name = categories[1];

        return result;
    }

    /**
     * Test de normalidad
     */
    testNormality(columnName) {
        const data = this.getNumericColumn(columnName);
        return Stats.normalityTest(data);
    }

    /**
     * Regresión lineal
     */
    performRegression(xColumn, yColumn) {
        const xData = this.getNumericColumn(xColumn);
        const yData = this.getNumericColumn(yColumn);

        // Emparejar datos (eliminar nulos)
        const paired = [];
        const minLength = Math.min(xData.length, yData.length);

        for (let i = 0; i < this.data.length; i++) {
            const x = parseFloat(this.data[i][xColumn]);
            const y = parseFloat(this.data[i][yColumn]);
            if (!isNaN(x) && !isNaN(y)) {
                paired.push({x, y});
            }
        }

        const x = paired.map(p => p.x);
        const y = paired.map(p => p.y);

        return Stats.linearRegression(x, y);
    }

    /**
     * Detecta outliers en una columna
     */
    findOutliers(columnName) {
        const data = this.getNumericColumn(columnName);
        return Stats.detectOutliers(data);
    }

    /**
     * Calcula intervalo de confianza
     */
    calculateConfidenceInterval(columnName, confidence = 0.95) {
        const data = this.getNumericColumn(columnName);
        return Stats.confidenceInterval(data, confidence);
    }

    /**
     * Prepara datos para histograma
     */
    prepareHistogramData(columnName, bins = 10) {
        const data = this.getNumericColumn(columnName);
        const min = Math.min(...data);
        const max = Math.max(...data);
        const binWidth = (max - min) / bins;

        const histogram = new Array(bins).fill(0);
        const binLabels = [];

        for (let i = 0; i < bins; i++) {
            const binStart = min + i * binWidth;
            const binEnd = binStart + binWidth;
            binLabels.push(`${binStart.toFixed(1)}-${binEnd.toFixed(1)}`);

            data.forEach(value => {
                if (value >= binStart && (i === bins - 1 ? value <= binEnd : value < binEnd)) {
                    histogram[i]++;
                }
            });
        }

        return {
            labels: binLabels,
            data: histogram
        };
    }

    /**
     * Prepara datos para gráfico de barras
     */
    prepareBarChartData(columnName, limit = 10) {
        const freqTable = Stats.frequencyTable(this.getColumn(columnName));
        const topN = freqTable.slice(0, limit);

        return {
            labels: topN.map(item => item.value),
            data: topN.map(item => item.count)
        };
    }

    /**
     * Prepara datos para gráfico de dispersión
     */
    prepareScatterData(xColumn, yColumn) {
        const data = [];

        this.data.forEach(row => {
            const x = parseFloat(row[xColumn]);
            const y = parseFloat(row[yColumn]);

            if (!isNaN(x) && !isNaN(y)) {
                data.push({x, y});
            }
        });

        return data;
    }

    /**
     * Prepara datos para gráfico de líneas (temporal)
     */
    prepareLineChartData(xColumn, yColumn) {
        const data = [];
        const labels = [];

        this.data.forEach(row => {
            const x = row[xColumn];
            const y = parseFloat(row[yColumn]);

            if (y !== null && !isNaN(y)) {
                labels.push(x);
                data.push(y);
            }
        });

        return {
            labels: labels,
            data: data
        };
    }

    /**
     * Exporta datos a CSV
     */
    exportToCSV() {
        if (!this.data || !this.headers) return null;

        const csv = Papa.unparse({
            fields: this.headers,
            data: this.data
        });

        return csv;
    }

    /**
     * Exporta estadísticas a CSV
     */
    exportStatistics() {
        const statsData = [];

        this.numericColumns.forEach(col => {
            const stats = this.calculateStats(col);
            statsData.push({
                variable: col,
                count: stats.count,
                mean: stats.mean.toFixed(2),
                median: stats.median.toFixed(2),
                std: stats.std.toFixed(2),
                min: stats.min.toFixed(2),
                max: stats.max.toFixed(2),
                q1: stats.q1.toFixed(2),
                q3: stats.q3.toFixed(2)
            });
        });

        const csv = Papa.unparse(statsData);
        return csv;
    }

    /**
     * Obtiene resumen del dataset
     */
    getSummary() {
        return {
            rows: this.data.length,
            columns: this.headers.length,
            numericColumns: this.numericColumns.length,
            categoricalColumns: this.categoricalColumns.length,
            columnNames: this.headers
        };
    }
}
