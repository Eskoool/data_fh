"""
Módulo de visualizaciones
Genera gráficos interactivos con Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import streamlit as st


class DataVisualizer:
    """Genera visualizaciones interactivas de datos farmacéuticos"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.color_palette = px.colors.qualitative.Set3

    def plot_histogram(self, column: str, bins: int = 30, title: str = None) -> go.Figure:
        """
        Histograma de una variable numérica

        Args:
            column: Nombre de la columna
            bins: Número de bins
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        fig = px.histogram(
            self.df,
            x=column,
            nbins=bins,
            title=title or f'Distribución de {column}',
            labels={column: column, 'count': 'Frecuencia'},
            color_discrete_sequence=self.color_palette
        )

        fig.update_layout(
            showlegend=False,
            hovermode='x unified'
        )

        return fig

    def plot_boxplot(self, columns: List[str], group_by: str = None, title: str = None) -> go.Figure:
        """
        Diagrama de cajas

        Args:
            columns: Columnas numéricas a visualizar
            group_by: Variable categórica para agrupar
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        if group_by:
            fig = px.box(
                self.df,
                y=columns[0],
                x=group_by,
                title=title or f'Diagrama de cajas de {columns[0]} por {group_by}',
                color=group_by,
                color_discrete_sequence=self.color_palette
            )
        else:
            fig = go.Figure()
            for col in columns:
                fig.add_trace(go.Box(y=self.df[col], name=col))

            fig.update_layout(
                title=title or 'Diagrama de cajas',
                yaxis_title='Valor'
            )

        return fig

    def plot_scatter(self, x: str, y: str, color: str = None, size: str = None,
                    title: str = None, trendline: bool = False) -> go.Figure:
        """
        Gráfico de dispersión

        Args:
            x: Variable eje X
            y: Variable eje Y
            color: Variable para colorear puntos
            size: Variable para tamaño de puntos
            title: Título del gráfico
            trendline: Añadir línea de tendencia

        Returns:
            Figura de Plotly
        """
        trendline_arg = "ols" if trendline else None

        fig = px.scatter(
            self.df,
            x=x,
            y=y,
            color=color,
            size=size,
            title=title or f'{y} vs {x}',
            trendline=trendline_arg,
            color_discrete_sequence=self.color_palette
        )

        fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))

        return fig

    def plot_correlation_matrix(self, columns: List[str] = None, method: str = 'pearson',
                                title: str = None) -> go.Figure:
        """
        Mapa de calor de correlaciones

        Args:
            columns: Columnas a correlacionar (None = todas numéricas)
            method: Método de correlación
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        if columns:
            df_subset = self.df[columns]
        else:
            df_subset = self.df.select_dtypes(include=[np.number])

        corr_matrix = df_subset.corr(method=method)

        fig = px.imshow(
            corr_matrix,
            title=title or f'Matriz de Correlación ({method.capitalize()})',
            labels=dict(color="Correlación"),
            color_continuous_scale='RdBu_r',
            aspect='auto',
            zmin=-1,
            zmax=1
        )

        fig.update_xaxes(side="bottom")

        return fig

    def plot_bar_chart(self, column: str, value_column: str = None,
                      aggregation: str = 'count', title: str = None) -> go.Figure:
        """
        Gráfico de barras

        Args:
            column: Variable categórica
            value_column: Variable numérica a agregar
            aggregation: Tipo de agregación ('count', 'sum', 'mean', 'median')
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        if aggregation == 'count':
            data = self.df[column].value_counts().reset_index()
            data.columns = [column, 'Frecuencia']
            y_col = 'Frecuencia'
        else:
            if value_column is None:
                raise ValueError("Debe especificar value_column para agregaciones distintas de 'count'")

            agg_dict = {
                'sum': 'sum',
                'mean': 'mean',
                'median': 'median'
            }

            data = self.df.groupby(column)[value_column].agg(agg_dict[aggregation]).reset_index()
            y_col = value_column

        fig = px.bar(
            data,
            x=column,
            y=y_col,
            title=title or f'{aggregation.capitalize()} de {y_col} por {column}',
            color_discrete_sequence=self.color_palette
        )

        fig.update_layout(xaxis_tickangle=-45)

        return fig

    def plot_line_chart(self, x: str, y: str, color: str = None, title: str = None) -> go.Figure:
        """
        Gráfico de líneas

        Args:
            x: Variable eje X (típicamente tiempo)
            y: Variable eje Y
            color: Variable para múltiples líneas
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        fig = px.line(
            self.df,
            x=x,
            y=y,
            color=color,
            title=title or f'Evolución de {y} en el tiempo',
            markers=True,
            color_discrete_sequence=self.color_palette
        )

        return fig

    def plot_pie_chart(self, column: str, title: str = None, top_n: int = None) -> go.Figure:
        """
        Gráfico circular

        Args:
            column: Variable categórica
            title: Título del gráfico
            top_n: Mostrar solo las N categorías más frecuentes

        Returns:
            Figura de Plotly
        """
        value_counts = self.df[column].value_counts()

        if top_n:
            value_counts = value_counts.head(top_n)

        fig = px.pie(
            values=value_counts.values,
            names=value_counts.index,
            title=title or f'Distribución de {column}',
            color_discrete_sequence=self.color_palette
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')

        return fig

    def plot_heatmap(self, x: str, y: str, value: str, aggregation: str = 'mean',
                    title: str = None) -> go.Figure:
        """
        Mapa de calor

        Args:
            x: Variable eje X
            y: Variable eje Y
            value: Variable de valor
            aggregation: Función de agregación
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        pivot_table = self.df.pivot_table(
            values=value,
            index=y,
            columns=x,
            aggfunc=aggregation
        )

        fig = px.imshow(
            pivot_table,
            title=title or f'{aggregation.capitalize()} de {value}',
            labels=dict(color=value),
            color_continuous_scale='Viridis',
            aspect='auto'
        )

        return fig

    def plot_violin(self, column: str, group_by: str = None, title: str = None) -> go.Figure:
        """
        Gráfico de violín

        Args:
            column: Variable numérica
            group_by: Variable categórica para agrupar
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        if group_by:
            fig = px.violin(
                self.df,
                y=column,
                x=group_by,
                title=title or f'Distribución de {column} por {group_by}',
                color=group_by,
                box=True,
                points='all',
                color_discrete_sequence=self.color_palette
            )
        else:
            fig = go.Figure()
            fig.add_trace(go.Violin(
                y=self.df[column],
                name=column,
                box_visible=True,
                meanline_visible=True
            ))

            fig.update_layout(
                title=title or f'Distribución de {column}',
                yaxis_title=column
            )

        return fig

    def plot_time_series(self, date_column: str, value_column: str,
                        decomposition: bool = False, title: str = None) -> go.Figure:
        """
        Gráfico de series temporales

        Args:
            date_column: Columna de fecha
            value_column: Columna de valores
            decomposition: Mostrar descomposición estacional
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        df_sorted = self.df.sort_values(date_column)

        if not decomposition:
            fig = px.line(
                df_sorted,
                x=date_column,
                y=value_column,
                title=title or f'Serie temporal de {value_column}',
                markers=True
            )
        else:
            # Descomposición simple (tendencia + estacionalidad)
            from statsmodels.tsa.seasonal import seasonal_decompose

            ts = df_sorted.set_index(date_column)[value_column]
            decomposition_result = seasonal_decompose(ts, model='additive', period=min(12, len(ts)//2))

            fig = make_subplots(
                rows=4, cols=1,
                subplot_titles=['Original', 'Tendencia', 'Estacionalidad', 'Residuos']
            )

            fig.add_trace(
                go.Scatter(x=ts.index, y=ts.values, name='Original'),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=ts.index, y=decomposition_result.trend, name='Tendencia'),
                row=2, col=1
            )
            fig.add_trace(
                go.Scatter(x=ts.index, y=decomposition_result.seasonal, name='Estacionalidad'),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=ts.index, y=decomposition_result.resid, name='Residuos'),
                row=4, col=1
            )

            fig.update_layout(height=800, title_text=title or "Descomposición de Serie Temporal")

        return fig

    def plot_3d_scatter(self, x: str, y: str, z: str, color: str = None, title: str = None) -> go.Figure:
        """
        Gráfico de dispersión 3D

        Args:
            x, y, z: Variables para los tres ejes
            color: Variable para colorear
            title: Título del gráfico

        Returns:
            Figura de Plotly
        """
        fig = px.scatter_3d(
            self.df,
            x=x,
            y=y,
            z=z,
            color=color,
            title=title or f'Gráfico 3D: {x}, {y}, {z}',
            color_discrete_sequence=self.color_palette
        )

        return fig
