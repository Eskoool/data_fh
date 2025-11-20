"""
Módulo de análisis estadístico
Realiza análisis estadísticos avanzados sobre los datos farmacéuticos
"""
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from typing import Dict, List, Tuple, Any
import warnings

warnings.filterwarnings('ignore')


class StatisticalAnalyzer:
    """Realiza análisis estadísticos sobre datos farmacéuticos"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.results = {}

    def descriptive_statistics(self, columns: List[str] = None) -> pd.DataFrame:
        """
        Calcula estadísticas descriptivas

        Args:
            columns: Columnas específicas a analizar (None = todas)

        Returns:
            DataFrame con estadísticas descriptivas
        """
        if columns:
            df_subset = self.df[columns]
        else:
            df_subset = self.df.select_dtypes(include=[np.number])

        stats_df = df_subset.describe().T
        stats_df['variance'] = df_subset.var()
        stats_df['cv'] = (df_subset.std() / df_subset.mean() * 100)  # Coeficiente de variación
        stats_df['skewness'] = df_subset.skew()
        stats_df['kurtosis'] = df_subset.kurtosis()

        return stats_df

    def correlation_analysis(self, columns: List[str] = None, method: str = 'pearson') -> pd.DataFrame:
        """
        Análisis de correlación entre variables

        Args:
            columns: Columnas a correlacionar
            method: 'pearson', 'spearman' o 'kendall'

        Returns:
            Matriz de correlación
        """
        if columns:
            df_subset = self.df[columns]
        else:
            df_subset = self.df.select_dtypes(include=[np.number])

        return df_subset.corr(method=method)

    def normality_test(self, column: str) -> Dict[str, Any]:
        """
        Test de normalidad (Shapiro-Wilk y Kolmogorov-Smirnov)

        Args:
            column: Nombre de la columna a testear

        Returns:
            Diccionario con resultados
        """
        data = self.df[column].dropna()

        # Shapiro-Wilk (mejor para muestras pequeñas n<50)
        shapiro_stat, shapiro_p = stats.shapiro(data)

        # Kolmogorov-Smirnov
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))

        return {
            'shapiro_statistic': shapiro_stat,
            'shapiro_pvalue': shapiro_p,
            'shapiro_normal': shapiro_p > 0.05,
            'ks_statistic': ks_stat,
            'ks_pvalue': ks_p,
            'ks_normal': ks_p > 0.05,
            'interpretation': 'Los datos siguen una distribución normal' if shapiro_p > 0.05 else 'Los datos NO siguen una distribución normal'
        }

    def t_test(self, column: str, group_column: str) -> Dict[str, Any]:
        """
        Prueba t de Student para comparar dos grupos

        Args:
            column: Variable numérica a comparar
            group_column: Variable categórica con 2 grupos

        Returns:
            Resultados de la prueba t
        """
        groups = self.df[group_column].unique()

        if len(groups) != 2:
            raise ValueError("La variable de grupo debe tener exactamente 2 categorías")

        group1 = self.df[self.df[group_column] == groups[0]][column].dropna()
        group2 = self.df[self.df[group_column] == groups[1]][column].dropna()

        # Test de Levene para homogeneidad de varianzas
        levene_stat, levene_p = stats.levene(group1, group2)

        # Prueba t (con o sin varianzas iguales)
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=(levene_p > 0.05))

        # Tamaño del efecto (d de Cohen)
        pooled_std = np.sqrt((group1.std()**2 + group2.std()**2) / 2)
        cohens_d = (group1.mean() - group2.mean()) / pooled_std

        return {
            'group1': groups[0],
            'group2': groups[1],
            'mean_group1': group1.mean(),
            'mean_group2': group2.mean(),
            'std_group1': group1.std(),
            'std_group2': group2.std(),
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'cohens_d': cohens_d,
            'effect_size': 'pequeño' if abs(cohens_d) < 0.5 else ('mediano' if abs(cohens_d) < 0.8 else 'grande'),
            'interpretation': f'Hay diferencia significativa entre {groups[0]} y {groups[1]}' if p_value < 0.05 else 'No hay diferencia significativa'
        }

    def anova_test(self, column: str, group_column: str) -> Dict[str, Any]:
        """
        ANOVA de un factor para comparar múltiples grupos

        Args:
            column: Variable numérica dependiente
            group_column: Variable categórica con grupos

        Returns:
            Resultados del ANOVA
        """
        groups = [group[column].dropna() for name, group in self.df.groupby(group_column)]

        # ANOVA
        f_stat, p_value = stats.f_oneway(*groups)

        # Test post-hoc de Tukey
        tukey_result = pairwise_tukeyhsd(
            self.df[column].dropna(),
            self.df.loc[self.df[column].notna(), group_column]
        )

        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'tukey_results': str(tukey_result),
            'interpretation': 'Al menos un grupo es significativamente diferente' if p_value < 0.05 else 'No hay diferencias significativas entre grupos'
        }

    def chi_square_test(self, column1: str, column2: str) -> Dict[str, Any]:
        """
        Test Chi-cuadrado para asociación entre variables categóricas

        Args:
            column1: Primera variable categórica
            column2: Segunda variable categórica

        Returns:
            Resultados del test Chi-cuadrado
        """
        contingency_table = pd.crosstab(self.df[column1], self.df[column2])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

        # V de Cramer (tamaño del efecto)
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape[0], contingency_table.shape[1]) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim))

        return {
            'chi2_statistic': chi2,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'cramers_v': cramers_v,
            'significant': p_value < 0.05,
            'contingency_table': contingency_table,
            'interpretation': f'Hay asociación significativa entre {column1} y {column2}' if p_value < 0.05 else 'No hay asociación significativa'
        }

    def linear_regression(self, target: str, features: List[str]) -> Dict[str, Any]:
        """
        Regresión lineal múltiple

        Args:
            target: Variable dependiente
            features: Variables independientes

        Returns:
            Resultados de la regresión
        """
        df_clean = self.df[[target] + features].dropna()
        X = df_clean[features]
        y = df_clean[target]

        # Añadir constante para el intercepto
        X_with_const = sm.add_constant(X)

        # Modelo de regresión
        model = sm.OLS(y, X_with_const).fit()

        # Predicciones
        predictions = model.predict(X_with_const)
        residuals = y - predictions

        return {
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'f_statistic': model.fvalue,
            'f_pvalue': model.f_pvalue,
            'coefficients': dict(zip(['Intercept'] + features, model.params)),
            'p_values': dict(zip(['Intercept'] + features, model.pvalues)),
            'std_errors': dict(zip(['Intercept'] + features, model.bse)),
            'residuals': residuals,
            'predictions': predictions,
            'summary': str(model.summary()),
            'interpretation': f'El modelo explica el {model.rsquared*100:.2f}% de la varianza de {target}'
        }

    def clustering_analysis(self, columns: List[str], n_clusters: int = 3) -> Dict[str, Any]:
        """
        Análisis de clustering (K-means)

        Args:
            columns: Variables para clustering
            n_clusters: Número de clusters

        Returns:
            Resultados del clustering
        """
        df_clean = self.df[columns].dropna()

        # Normalizar datos
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_clean)

        # K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        # Estadísticas por cluster
        df_clean['Cluster'] = clusters
        cluster_stats = df_clean.groupby('Cluster')[columns].mean()

        return {
            'clusters': clusters,
            'cluster_centers': kmeans.cluster_centers_,
            'inertia': kmeans.inertia_,
            'cluster_stats': cluster_stats,
            'n_samples_per_cluster': pd.Series(clusters).value_counts().to_dict(),
            'interpretation': f'Los datos se han agrupado en {n_clusters} clusters'
        }

    def pca_analysis(self, columns: List[str], n_components: int = 2) -> Dict[str, Any]:
        """
        Análisis de Componentes Principales (PCA)

        Args:
            columns: Variables para PCA
            n_components: Número de componentes

        Returns:
            Resultados del PCA
        """
        df_clean = self.df[columns].dropna()

        # Normalizar
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_clean)

        # PCA
        pca = PCA(n_components=n_components)
        components = pca.fit_transform(X_scaled)

        return {
            'explained_variance_ratio': pca.explained_variance_ratio_,
            'cumulative_variance': np.cumsum(pca.explained_variance_ratio_),
            'components': components,
            'loadings': pd.DataFrame(
                pca.components_.T,
                columns=[f'PC{i+1}' for i in range(n_components)],
                index=columns
            ),
            'interpretation': f'Los primeros {n_components} componentes explican el {sum(pca.explained_variance_ratio_)*100:.2f}% de la varianza'
        }

    def predictive_model(self, target: str, features: List[str], model_type: str = 'regression') -> Dict[str, Any]:
        """
        Modelo predictivo con Random Forest

        Args:
            target: Variable objetivo
            features: Variables predictoras
            model_type: 'regression' o 'classification'

        Returns:
            Resultados del modelo
        """
        df_clean = self.df[[target] + features].dropna()
        X = df_clean[features]
        y = df_clean[target]

        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if model_type == 'regression':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

            r2 = r2_score(y_test, predictions)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))

            return {
                'model_type': 'Random Forest Regression',
                'r2_score': r2,
                'rmse': rmse,
                'feature_importance': dict(zip(features, model.feature_importances_)),
                'predictions': predictions,
                'actual': y_test.values,
                'interpretation': f'El modelo tiene un R² de {r2:.3f} (explica el {r2*100:.1f}% de la varianza)'
            }
        else:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

            accuracy = accuracy_score(y_test, predictions)

            return {
                'model_type': 'Random Forest Classification',
                'accuracy': accuracy,
                'classification_report': classification_report(y_test, predictions),
                'feature_importance': dict(zip(features, model.feature_importances_)),
                'predictions': predictions,
                'actual': y_test.values,
                'interpretation': f'El modelo tiene una precisión del {accuracy*100:.1f}%'
            }
