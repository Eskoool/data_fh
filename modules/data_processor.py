"""
Módulo de procesamiento de datos
Maneja la carga y preparación de archivos CSV/Excel
"""
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
import streamlit as st


class DataProcessor:
    """Procesa archivos de datos farmacéuticos"""

    def __init__(self):
        self.df = None
        self.file_name = None

    def load_file(self, uploaded_file) -> pd.DataFrame:
        """
        Carga un archivo CSV o Excel

        Args:
            uploaded_file: Archivo subido por Streamlit

        Returns:
            DataFrame de pandas
        """
        try:
            self.file_name = uploaded_file.name

            if uploaded_file.name.endswith('.csv'):
                # Intentar detectar el delimitador
                self.df = pd.read_csv(uploaded_file, encoding='utf-8')
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(uploaded_file)
            else:
                raise ValueError("Formato de archivo no soportado")

            return self.df

        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")
            return None

    def get_data_summary(self) -> Dict:
        """Obtiene un resumen de los datos"""
        if self.df is None:
            return {}

        summary = {
            "n_rows": len(self.df),
            "n_columns": len(self.df.columns),
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "memory_usage": self.df.memory_usage(deep=True).sum() / 1024**2  # MB
        }

        return summary

    def identify_variable_types(self) -> Dict[str, List[str]]:
        """
        Identifica tipos de variables: numéricas, categóricas, fechas

        Returns:
            Diccionario con listas de nombres de columnas por tipo
        """
        if self.df is None:
            return {}

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()

        # Intentar detectar fechas en columnas de texto
        for col in categorical_cols[:]:
            try:
                pd.to_datetime(self.df[col].dropna().head(100))
                datetime_cols.append(col)
                categorical_cols.remove(col)
            except:
                pass

        return {
            "numericas": numeric_cols,
            "categoricas": categorical_cols,
            "fechas": datetime_cols
        }

    def clean_data(self, drop_duplicates: bool = False,
                   drop_na: bool = False,
                   fill_na_method: str = None) -> pd.DataFrame:
        """
        Limpia los datos según las opciones especificadas

        Args:
            drop_duplicates: Eliminar filas duplicadas
            drop_na: Eliminar filas con valores nulos
            fill_na_method: Método para rellenar nulos ('mean', 'median', 'mode', 'forward', 'backward')

        Returns:
            DataFrame limpio
        """
        if self.df is None:
            return None

        df_clean = self.df.copy()

        if drop_duplicates:
            df_clean = df_clean.drop_duplicates()

        if drop_na:
            df_clean = df_clean.dropna()
        elif fill_na_method:
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns

            if fill_na_method == 'mean':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
            elif fill_na_method == 'median':
                df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
            elif fill_na_method == 'mode':
                for col in df_clean.columns:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else None)
            elif fill_na_method == 'forward':
                df_clean = df_clean.fillna(method='ffill')
            elif fill_na_method == 'backward':
                df_clean = df_clean.fillna(method='bfill')

        return df_clean

    def get_basic_statistics(self) -> pd.DataFrame:
        """Obtiene estadísticas descriptivas básicas"""
        if self.df is None:
            return None

        return self.df.describe(include='all')

    def suggest_analyses(self, objective: str) -> List[str]:
        """
        Sugiere análisis según el objetivo del usuario

        Args:
            objective: Objetivo del análisis (ej: "comparar ventas", "predecir demanda")

        Returns:
            Lista de análisis sugeridos
        """
        suggestions = []
        var_types = self.identify_variable_types()

        objective_lower = objective.lower()

        # Análisis basados en el objetivo
        if any(word in objective_lower for word in ["comparar", "diferencia", "entre"]):
            if len(var_types["numericas"]) > 0 and len(var_types["categoricas"]) > 0:
                suggestions.append("Análisis de Varianza (ANOVA)")
                suggestions.append("Prueba t de Student")
                suggestions.append("Comparación de medias por grupos")

        if any(word in objective_lower for word in ["relación", "correlación", "asociación"]):
            if len(var_types["numericas"]) >= 2:
                suggestions.append("Análisis de Correlación")
                suggestions.append("Matriz de Correlaciones")
                suggestions.append("Regresión Lineal")

        if any(word in objective_lower for word in ["predecir", "predicción", "forecast"]):
            suggestions.append("Regresión Lineal/Múltiple")
            suggestions.append("Modelos de Machine Learning")
            if len(var_types["fechas"]) > 0:
                suggestions.append("Series Temporales (ARIMA)")

        if any(word in objective_lower for word in ["clasificar", "categorizar", "agrupar"]):
            suggestions.append("Análisis de Clustering (K-means)")
            suggestions.append("Análisis Discriminante")

        if any(word in objective_lower for word in ["tendencia", "evolución", "tiempo"]):
            if len(var_types["fechas"]) > 0:
                suggestions.append("Análisis de Tendencias")
                suggestions.append("Series Temporales")
                suggestions.append("Descomposición Estacional")

        # Análisis generales siempre disponibles
        suggestions.append("Estadísticas Descriptivas")
        suggestions.append("Visualizaciones Exploratorias")

        return list(set(suggestions))  # Eliminar duplicados
