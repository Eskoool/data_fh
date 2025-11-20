"""
Aplicación de Análisis de Datos Farmacéuticos
Sistema interactivo y minimalista compatible con RGPD
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Añadir el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from config import *
from modules.data_processor import DataProcessor
from modules.statistical_analyzer import StatisticalAnalyzer
from modules.ai_assistant import AIAssistant
from modules.visualizations import DataVisualizer

# Configuración de la página
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para diseño minimalista
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    h1 {
        color: #1f77b4;
        font-weight: 600;
    }
    h2 {
        color: #2c3e50;
        font-weight: 500;
        font-size: 1.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = DataProcessor()
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant(
            model=OLLAMA_MODEL,
            host=OLLAMA_HOST
        )
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def main():
    """Función principal de la aplicación"""
    initialize_session_state()

    # Encabezado
    st.title("💊 " + APP_TITLE)
    st.markdown(f"*{APP_DESCRIPTION}*")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")

        # Información RGPD
        with st.expander("🔒 Protección de Datos (RGPD)", expanded=False):
            st.success("""
            ✅ **Cumplimiento RGPD**
            - Todos los datos se procesan localmente
            - No se envía información a servidores externos
            - Los archivos se eliminan automáticamente al cerrar la sesión
            - No se almacenan datos personales
            """)

        st.markdown("---")

        # Carga de archivo
        st.subheader("📁 Cargar Datos")
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV o Excel",
            type=['csv', 'xlsx', 'xls'],
            help="Tamaño máximo: 100MB"
        )

        if uploaded_file is not None:
            if st.button("🔄 Cargar Archivo", type="primary"):
                with st.spinner("Cargando datos..."):
                    df = st.session_state.data_processor.load_file(uploaded_file)
                    if df is not None:
                        st.session_state.df = df
                        st.success(f"✅ Archivo cargado: {uploaded_file.name}")
                        st.info(f"**Filas:** {len(df)} | **Columnas:** {len(df.columns)}")

        # Ejemplos de datos
        st.markdown("---")
        if st.button("📊 Usar Datos de Ejemplo"):
            # Cargar datos de ejemplo si existen
            example_files = list(EXAMPLES_DIR.glob("*.csv")) + list(EXAMPLES_DIR.glob("*.xlsx"))
            if example_files:
                example_file = example_files[0]
                st.session_state.df = pd.read_csv(example_file) if example_file.suffix == '.csv' else pd.read_excel(example_file)
                st.success(f"✅ Datos de ejemplo cargados")
            else:
                # Crear datos de ejemplo si no existen
                df_example = create_example_data()
                st.session_state.df = df_example
                st.success("✅ Datos de ejemplo generados")

        # IA Assistant status
        st.markdown("---")
        st.subheader("🤖 Asistente IA")
        if st.session_state.ai_assistant.available:
            st.success("✅ Disponible (Ollama)")
        else:
            st.warning("⚠️ No disponible")
            st.caption("Instala Ollama para usar IA generativa")

    # Contenido principal
    if st.session_state.df is not None:
        df = st.session_state.df

        # Tabs principales
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Exploración",
            "📈 Análisis Estadístico",
            "🔮 Modelos Predictivos",
            "🤖 Asistente IA",
            "💾 Exportar"
        ])

        with tab1:
            show_exploration_tab(df)

        with tab2:
            show_statistical_analysis_tab(df)

        with tab3:
            show_predictive_models_tab(df)

        with tab4:
            show_ai_assistant_tab(df)

        with tab5:
            show_export_tab(df)

    else:
        # Pantalla de bienvenida
        st.info("👈 Comienza cargando un archivo de datos o usando datos de ejemplo desde el panel lateral")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            ### 📊 Análisis Exploratorio
            - Estadísticas descriptivas
            - Visualizaciones interactivas
            - Detección de patrones
            """)

        with col2:
            st.markdown("""
            ### 📈 Análisis Estadístico
            - Pruebas de hipótesis
            - Correlaciones
            - ANOVA, regresión
            """)

        with col3:
            st.markdown("""
            ### 🤖 IA Asistente
            - Interpretación automática
            - Sugerencias de análisis
            - Chat interactivo
            """)


def show_exploration_tab(df):
    """Muestra la pestaña de exploración de datos"""
    st.header("📊 Exploración de Datos")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Filas", f"{len(df):,}")
    with col2:
        st.metric("Columnas", len(df.columns))
    with col3:
        st.metric("Valores Nulos", f"{df.isnull().sum().sum():,}")
    with col4:
        st.metric("Memoria", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Vista previa de datos
    st.subheader("Vista Previa")
    n_rows = st.slider("Número de filas a mostrar", 5, 100, 10)
    st.dataframe(df.head(n_rows), use_container_width=True)

    # Información de columnas
    st.subheader("Información de Columnas")
    col_info = pd.DataFrame({
        'Tipo': df.dtypes,
        'Valores Únicos': df.nunique(),
        'Nulos': df.isnull().sum(),
        '% Nulos': (df.isnull().sum() / len(df) * 100).round(2)
    })
    st.dataframe(col_info, use_container_width=True)

    # Estadísticas descriptivas
    st.subheader("Estadísticas Descriptivas")
    processor = DataProcessor()
    processor.df = df
    stats = processor.get_basic_statistics()
    st.dataframe(stats, use_container_width=True)

    # Visualizaciones básicas
    st.subheader("Visualizaciones")

    visualizer = DataVisualizer(df)
    var_types = processor.identify_variable_types()

    col1, col2 = st.columns(2)

    with col1:
        if var_types['numericas']:
            selected_num = st.selectbox("Variable numérica", var_types['numericas'])
            fig = visualizer.plot_histogram(selected_num)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if var_types['categoricas']:
            selected_cat = st.selectbox("Variable categórica", var_types['categoricas'])
            fig = visualizer.plot_bar_chart(selected_cat)
            st.plotly_chart(fig, use_container_width=True)


def show_statistical_analysis_tab(df):
    """Muestra la pestaña de análisis estadístico"""
    st.header("📈 Análisis Estadístico")

    analyzer = StatisticalAnalyzer(df)
    processor = DataProcessor()
    processor.df = df
    var_types = processor.identify_variable_types()

    # Selector de tipo de análisis
    analysis_type = st.selectbox(
        "Selecciona el tipo de análisis",
        [
            "Correlaciones",
            "Prueba t de Student",
            "ANOVA",
            "Chi-cuadrado",
            "Regresión Lineal",
            "Test de Normalidad",
            "Clustering (K-means)",
            "PCA"
        ]
    )

    st.markdown("---")

    if analysis_type == "Correlaciones":
        st.subheader("Matriz de Correlaciones")
        if var_types['numericas']:
            selected_vars = st.multiselect("Variables", var_types['numericas'], default=var_types['numericas'][:5])
            method = st.radio("Método", ['pearson', 'spearman', 'kendall'])

            if selected_vars and st.button("Calcular"):
                corr_matrix = analyzer.correlation_analysis(selected_vars, method)
                visualizer = DataVisualizer(df)
                fig = visualizer.plot_correlation_matrix(selected_vars, method)
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(corr_matrix, use_container_width=True)

                # Interpretación IA
                if st.session_state.ai_assistant.available:
                    with st.expander("🤖 Interpretación IA"):
                        interpretation = st.session_state.ai_assistant.interpret_correlation(corr_matrix)
                        st.write(interpretation)

    elif analysis_type == "Prueba t de Student":
        st.subheader("Comparación de Medias (2 grupos)")
        col1, col2 = st.columns(2)
        with col1:
            numeric_var = st.selectbox("Variable numérica", var_types['numericas'])
        with col2:
            cat_var = st.selectbox("Variable categórica (2 grupos)", var_types['categoricas'])

        if st.button("Realizar Test"):
            try:
                results = analyzer.t_test(numeric_var, cat_var)
                st.success(results['interpretation'])

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(f"Media {results['group1']}", f"{results['mean_group1']:.2f}")
                with col2:
                    st.metric(f"Media {results['group2']}", f"{results['mean_group2']:.2f}")
                with col3:
                    st.metric("p-valor", f"{results['p_value']:.4f}")

                st.info(f"**Tamaño del efecto (d de Cohen):** {results['cohens_d']:.3f} ({results['effect_size']})")

                # Visualización
                visualizer = DataVisualizer(df)
                fig = visualizer.plot_boxplot([numeric_var], group_by=cat_var)
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    elif analysis_type == "ANOVA":
        st.subheader("Análisis de Varianza (ANOVA)")
        col1, col2 = st.columns(2)
        with col1:
            numeric_var = st.selectbox("Variable dependiente", var_types['numericas'])
        with col2:
            cat_var = st.selectbox("Variable de grupo", var_types['categoricas'])

        if st.button("Realizar ANOVA"):
            try:
                results = analyzer.anova_test(numeric_var, cat_var)
                st.success(results['interpretation'])

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("F-estadístico", f"{results['f_statistic']:.2f}")
                with col2:
                    st.metric("p-valor", f"{results['p_value']:.4f}")

                st.text("Test post-hoc de Tukey:")
                st.text(results['tukey_results'])

                # Visualización
                visualizer = DataVisualizer(df)
                fig = visualizer.plot_boxplot([numeric_var], group_by=cat_var)
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

    elif analysis_type == "Regresión Lineal":
        st.subheader("Regresión Lineal Múltiple")
        target = st.selectbox("Variable dependiente (Y)", var_types['numericas'])
        features = st.multiselect("Variables independientes (X)", [v for v in var_types['numericas'] if v != target])

        if features and st.button("Ajustar Modelo"):
            try:
                results = analyzer.linear_regression(target, features)
                st.success(results['interpretation'])

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("R²", f"{results['r_squared']:.3f}")
                with col2:
                    st.metric("R² ajustado", f"{results['adj_r_squared']:.3f}")
                with col3:
                    st.metric("p-valor (F)", f"{results['f_pvalue']:.4f}")

                st.subheader("Coeficientes")
                coef_df = pd.DataFrame({
                    'Coeficiente': results['coefficients'],
                    'p-valor': results['p_values']
                })
                st.dataframe(coef_df, use_container_width=True)

                with st.expander("📊 Resumen Completo"):
                    st.text(results['summary'])

            except Exception as e:
                st.error(f"Error: {str(e)}")

    elif analysis_type == "Clustering (K-means)":
        st.subheader("Análisis de Clustering")
        selected_vars = st.multiselect("Variables para clustering", var_types['numericas'])
        n_clusters = st.slider("Número de clusters", 2, 10, 3)

        if selected_vars and st.button("Ejecutar Clustering"):
            try:
                results = analyzer.clustering_analysis(selected_vars, n_clusters)
                st.success(results['interpretation'])

                st.subheader("Características de los Clusters")
                st.dataframe(results['cluster_stats'], use_container_width=True)

                st.metric("Inercia", f"{results['inertia']:.2f}")

                # Visualización 2D o 3D
                if len(selected_vars) >= 2:
                    visualizer = DataVisualizer(df.copy())
                    visualizer.df['Cluster'] = results['clusters']
                    if len(selected_vars) == 2:
                        fig = visualizer.plot_scatter(selected_vars[0], selected_vars[1], color='Cluster')
                    else:
                        fig = visualizer.plot_3d_scatter(selected_vars[0], selected_vars[1], selected_vars[2], color='Cluster')
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")


def show_predictive_models_tab(df):
    """Muestra la pestaña de modelos predictivos"""
    st.header("🔮 Modelos Predictivos")

    processor = DataProcessor()
    processor.df = df
    var_types = processor.identify_variable_types()

    st.info("📊 Los modelos utilizan Random Forest para predicciones robustas")

    model_type = st.radio("Tipo de modelo", ["Regresión", "Clasificación"])

    target = st.selectbox("Variable objetivo", df.columns)
    features = st.multiselect("Variables predictoras", [col for col in var_types['numericas'] if col != target])

    if features and st.button("Entrenar Modelo", type="primary"):
        try:
            analyzer = StatisticalAnalyzer(df)

            with st.spinner("Entrenando modelo..."):
                results = analyzer.predictive_model(
                    target,
                    features,
                    model_type='regression' if model_type == "Regresión" else 'classification'
                )

            st.success(results['interpretation'])

            col1, col2 = st.columns(2)
            with col1:
                if model_type == "Regresión":
                    st.metric("R² Score", f"{results['r2_score']:.3f}")
                    st.metric("RMSE", f"{results['rmse']:.3f}")
                else:
                    st.metric("Accuracy", f"{results['accuracy']:.3f}")

            with col2:
                st.subheader("Importancia de Variables")
                importance_df = pd.DataFrame({
                    'Variable': list(results['feature_importance'].keys()),
                    'Importancia': list(results['feature_importance'].values())
                }).sort_values('Importancia', ascending=False)
                st.dataframe(importance_df, use_container_width=True)

            # Gráfico de predicciones vs reales
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=results['actual'],
                y=results['predictions'],
                mode='markers',
                name='Predicciones'
            ))
            fig.add_trace(go.Scatter(
                x=[min(results['actual']), max(results['actual'])],
                y=[min(results['actual']), max(results['actual'])],
                mode='lines',
                name='Línea perfecta',
                line=dict(dash='dash', color='red')
            ))
            fig.update_layout(
                title="Predicciones vs Valores Reales",
                xaxis_title="Valores Reales",
                yaxis_title="Predicciones"
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error al entrenar modelo: {str(e)}")


def show_ai_assistant_tab(df):
    """Muestra la pestaña del asistente IA"""
    st.header("🤖 Asistente IA")

    if not st.session_state.ai_assistant.available:
        st.warning("""
        ⚠️ **Asistente IA no disponible**

        Para usar esta función, necesitas instalar Ollama:

        1. Descarga Ollama: https://ollama.ai/download
        2. Instala y ejecuta: `ollama run mistral`
        3. Reinicia esta aplicación

        **Nota:** Ollama se ejecuta completamente en local, cumpliendo con RGPD.
        """)
        return

    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Análisis Sugerido", "❓ Ayuda"])

    with tab1:
        st.subheader("Chat con el Asistente")

        # Mostrar historial
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.write(msg['content'])

        # Input del usuario
        user_input = st.chat_input("Pregunta algo sobre tus datos...")

        if user_input:
            # Añadir mensaje del usuario
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})

            with st.chat_message("user"):
                st.write(user_input)

            # Generar respuesta
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = st.session_state.ai_assistant.chat(user_input, st.session_state.chat_history)
                    st.write(response)

            st.session_state.chat_history.append({'role': 'assistant', 'content': response})

        if st.button("🗑️ Limpiar chat"):
            st.session_state.chat_history = []
            st.rerun()

    with tab2:
        st.subheader("Análisis Sugerido")

        objective = st.text_area("¿Qué quieres analizar?", placeholder="Ej: Quiero comparar las ventas entre diferentes categorías de productos")

        if st.button("Obtener Sugerencias"):
            processor = DataProcessor()
            processor.df = df
            data_summary = processor.get_data_summary()
            data_summary['variable_types'] = processor.identify_variable_types()

            with st.spinner("Analizando..."):
                suggestions = st.session_state.ai_assistant.suggest_analysis(data_summary, objective)
                st.write(suggestions)

    with tab3:
        st.subheader("Ayuda con Conceptos")

        concept = st.selectbox(
            "Selecciona un concepto",
            [
                "Correlación de Pearson",
                "Prueba t de Student",
                "ANOVA",
                "Regresión lineal",
                "Chi-cuadrado",
                "p-valor",
                "Intervalo de confianza",
                "d de Cohen",
                "R cuadrado",
                "K-means clustering"
            ]
        )

        if st.button("Explicar"):
            with st.spinner("Generando explicación..."):
                explanation = st.session_state.ai_assistant.explain_concept(concept)
                st.info(explanation)


def show_export_tab(df):
    """Muestra la pestaña de exportación"""
    st.header("💾 Exportar Resultados")

    st.info("🔒 Los datos exportados permanecen en tu equipo local")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Exportar Datos")

        # CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Descargar CSV",
            data=csv,
            file_name="datos_farmacia.csv",
            mime="text/csv"
        )

        # Excel
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
        buffer.seek(0)

        st.download_button(
            label="📊 Descargar Excel",
            data=buffer,
            file_name="datos_farmacia.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        st.subheader("Estadísticas")

        processor = DataProcessor()
        processor.df = df
        stats = processor.get_basic_statistics()

        stats_csv = stats.to_csv().encode('utf-8')
        st.download_button(
            label="📈 Descargar Estadísticas",
            data=stats_csv,
            file_name="estadisticas.csv",
            mime="text/csv"
        )


def create_example_data():
    """Crea datos de ejemplo de una farmacia"""
    np.random.seed(42)
    n = 500

    df = pd.DataFrame({
        'fecha': pd.date_range('2023-01-01', periods=n, freq='D'),
        'ventas_euros': np.random.normal(1500, 300, n),
        'num_clientes': np.random.poisson(50, n),
        'categoria': np.random.choice(['Medicamentos', 'Cosmetica', 'Higiene', 'Nutricion'], n),
        'prescripcion': np.random.choice(['Si', 'No'], n, p=[0.6, 0.4]),
        'satisfaccion': np.random.randint(1, 6, n),
        'edad_promedio': np.random.normal(45, 15, n),
        'temperatura': np.random.normal(20, 5, n)
    })

    # Añadir correlación artificial
    df['ventas_euros'] = df['ventas_euros'] + df['num_clientes'] * 10 + np.random.normal(0, 100, n)

    return df


if __name__ == "__main__":
    main()
