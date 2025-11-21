/**
 * Funciones estadísticas complementarias
 * Extiende simple-statistics con funciones adicionales
 */

const Stats = {
    /**
     * Calcula estadísticas descriptivas completas
     */
    descriptiveStats: function(data) {
        if (!data || data.length === 0) return null;

        const sorted = data.slice().sort((a, b) => a - b);
        const n = data.length;

        return {
            count: n,
            mean: ss.mean(data),
            median: ss.median(data),
            mode: ss.mode(data),
            min: ss.min(data),
            max: ss.max(data),
            range: ss.max(data) - ss.min(data),
            variance: ss.variance(data),
            std: ss.standardDeviation(data),
            q1: ss.quantile(data, 0.25),
            q3: ss.quantile(data, 0.75),
            iqr: ss.quantile(data, 0.75) - ss.quantile(data, 0.25),
            skewness: this.skewness(data),
            kurtosis: this.kurtosis(data),
            cv: (ss.standardDeviation(data) / ss.mean(data)) * 100 // Coeficiente de variación
        };
    },

    /**
     * Calcula la asimetría (skewness)
     */
    skewness: function(data) {
        const n = data.length;
        const mean = ss.mean(data);
        const std = ss.standardDeviation(data);

        const sum = data.reduce((acc, val) => {
            return acc + Math.pow((val - mean) / std, 3);
        }, 0);

        return (n / ((n - 1) * (n - 2))) * sum;
    },

    /**
     * Calcula la curtosis
     */
    kurtosis: function(data) {
        const n = data.length;
        const mean = ss.mean(data);
        const std = ss.standardDeviation(data);

        const sum = data.reduce((acc, val) => {
            return acc + Math.pow((val - mean) / std, 4);
        }, 0);

        return ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * sum -
               (3 * Math.pow(n - 1, 2)) / ((n - 2) * (n - 3));
    },

    /**
     * Prueba t de Student para una muestra
     */
    tTest: function(data, populationMean) {
        const n = data.length;
        const mean = ss.mean(data);
        const std = ss.standardDeviation(data);
        const se = std / Math.sqrt(n);
        const t = (mean - populationMean) / se;
        const df = n - 1;

        return {
            t: t,
            df: df,
            mean: mean,
            std: std,
            se: se,
            significant: Math.abs(t) > 1.96 // Aproximación para α=0.05
        };
    },

    /**
     * Prueba t de Student para dos muestras independientes
     */
    tTestTwoSample: function(data1, data2) {
        const n1 = data1.length;
        const n2 = data2.length;
        const mean1 = ss.mean(data1);
        const mean2 = ss.mean(data2);
        const var1 = ss.variance(data1);
        const var2 = ss.variance(data2);

        // Varianza pooled
        const pooledVar = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2);
        const se = Math.sqrt(pooledVar * (1/n1 + 1/n2));
        const t = (mean1 - mean2) / se;
        const df = n1 + n2 - 2;

        // Cohen's d (tamaño del efecto)
        const cohensD = (mean1 - mean2) / Math.sqrt(pooledVar);

        return {
            t: t,
            df: df,
            mean1: mean1,
            mean2: mean2,
            std1: Math.sqrt(var1),
            std2: Math.sqrt(var2),
            cohensD: cohensD,
            effectSize: Math.abs(cohensD) < 0.5 ? 'pequeño' : (Math.abs(cohensD) < 0.8 ? 'mediano' : 'grande'),
            significant: Math.abs(t) > 1.96, // Aproximación
            interpretation: Math.abs(t) > 1.96 ? 'Hay diferencia significativa' : 'No hay diferencia significativa'
        };
    },

    /**
     * Matriz de correlación de Pearson
     */
    correlationMatrix: function(dataMatrix) {
        const n = dataMatrix.length; // número de variables
        const matrix = [];

        for (let i = 0; i < n; i++) {
            matrix[i] = [];
            for (let j = 0; j < n; j++) {
                if (i === j) {
                    matrix[i][j] = 1.0;
                } else {
                    matrix[i][j] = ss.sampleCorrelation(dataMatrix[i], dataMatrix[j]);
                }
            }
        }

        return matrix;
    },

    /**
     * Test de normalidad (Shapiro-Wilk simplificado)
     * Nota: Implementación aproximada, para datos pequeños
     */
    normalityTest: function(data) {
        const n = data.length;
        const sorted = data.slice().sort((a, b) => a - b);
        const mean = ss.mean(data);

        // Calcular W estadístico (versión simplificada)
        let numerator = 0;
        let denominator = 0;

        for (let i = 0; i < n; i++) {
            denominator += Math.pow(sorted[i] - mean, 2);
        }

        // Aproximación simple
        const variance = ss.variance(data);
        const std = Math.sqrt(variance);

        // Test de asimetría y curtosis
        const skew = Math.abs(this.skewness(data));
        const kurt = Math.abs(this.kurtosis(data));

        const isNormal = skew < 2 && kurt < 7; // Criterios aproximados

        return {
            skewness: this.skewness(data),
            kurtosis: this.kurtosis(data),
            isNormal: isNormal,
            interpretation: isNormal ?
                'Los datos parecen seguir una distribución normal' :
                'Los datos NO parecen seguir una distribución normal',
            recommendation: isNormal ?
                'Puedes usar pruebas paramétricas (t-test, ANOVA)' :
                'Considera usar pruebas no paramétricas'
        };
    },

    /**
     * Análisis de frecuencias para variables categóricas
     */
    frequencyTable: function(data) {
        const freq = {};
        let total = 0;

        data.forEach(val => {
            freq[val] = (freq[val] || 0) + 1;
            total++;
        });

        // Convertir a array ordenado
        const table = Object.entries(freq)
            .map(([value, count]) => ({
                value: value,
                count: count,
                percentage: (count / total * 100).toFixed(2),
                cumulative: 0
            }))
            .sort((a, b) => b.count - a.count);

        // Calcular acumulado
        let cumSum = 0;
        table.forEach(item => {
            cumSum += parseFloat(item.percentage);
            item.cumulative = cumSum.toFixed(2);
        });

        return table;
    },

    /**
     * Detecta outliers usando el método IQR
     */
    detectOutliers: function(data) {
        const q1 = ss.quantile(data, 0.25);
        const q3 = ss.quantile(data, 0.75);
        const iqr = q3 - q1;
        const lowerBound = q1 - 1.5 * iqr;
        const upperBound = q3 + 1.5 * iqr;

        const outliers = data.filter(val => val < lowerBound || val > upperBound);

        return {
            lowerBound: lowerBound,
            upperBound: upperBound,
            outliers: outliers,
            count: outliers.length,
            percentage: (outliers.length / data.length * 100).toFixed(2)
        };
    },

    /**
     * Calcula intervalos de confianza
     */
    confidenceInterval: function(data, confidence = 0.95) {
        const mean = ss.mean(data);
        const std = ss.standardDeviation(data);
        const n = data.length;
        const se = std / Math.sqrt(n);

        // Valor crítico (aproximación para distribución normal)
        const z = confidence === 0.95 ? 1.96 : (confidence === 0.99 ? 2.576 : 1.645);

        const margin = z * se;

        return {
            mean: mean,
            lower: mean - margin,
            upper: mean + margin,
            margin: margin,
            confidence: confidence * 100
        };
    },

    /**
     * Regresión lineal simple
     */
    linearRegression: function(x, y) {
        const n = x.length;
        const regression = ss.linearRegression([x, y]);
        const line = ss.linearRegressionLine(regression);

        // Calcular R²
        const yMean = ss.mean(y);
        let ssTotal = 0;
        let ssResidual = 0;

        for (let i = 0; i < n; i++) {
            const yPred = line(x[i]);
            ssTotal += Math.pow(y[i] - yMean, 2);
            ssResidual += Math.pow(y[i] - yPred, 2);
        }

        const r2 = 1 - (ssResidual / ssTotal);
        const r = ss.sampleCorrelation(x, y);

        return {
            slope: regression.m,
            intercept: regression.b,
            r: r,
            r2: r2,
            predict: line,
            interpretation: `El modelo explica el ${(r2 * 100).toFixed(2)}% de la varianza`
        };
    },

    /**
     * Formatea un número para mostrar
     */
    formatNumber: function(num, decimals = 2) {
        if (num === null || num === undefined || isNaN(num)) return '-';
        return Number(num).toFixed(decimals);
    },

    /**
     * Determina si una variable es numérica
     */
    isNumeric: function(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    }
};
