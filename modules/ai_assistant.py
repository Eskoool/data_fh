"""
Módulo de asistente IA generativo
Usa modelos locales (Ollama) para asistir en el análisis de datos
"""
import json
from typing import Dict, List, Any, Optional
import pandas as pd

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class AIAssistant:
    """Asistente IA para análisis de datos farmacéuticos"""

    def __init__(self, model: str = "mistral", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.available = OLLAMA_AVAILABLE and self._check_ollama_connection()

    def _check_ollama_connection(self) -> bool:
        """Verifica si Ollama está disponible"""
        try:
            ollama.list()
            return True
        except Exception as e:
            print(f"Ollama no disponible: {e}")
            return False

    def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Genera una respuesta usando el modelo de IA

        Args:
            prompt: Pregunta o solicitud del usuario
            context: Contexto adicional (datos, resultados, etc.)

        Returns:
            Respuesta del modelo
        """
        if not self.available:
            return "⚠️ El asistente IA no está disponible. Instala Ollama para usar esta función.\n\n" \
                   "Instrucciones: https://ollama.ai/download"

        try:
            full_prompt = f"""Eres un asistente experto en análisis de datos farmacéuticos y estadística.
Tu objetivo es ayudar a profesionales de farmacia a entender y analizar sus datos.

IMPORTANTE:
- Responde en español de forma clara y concisa
- Usa lenguaje técnico pero accesible
- Proporciona interpretaciones prácticas
- Sugiere acciones basadas en los datos

Contexto de los datos:
{context}

Pregunta del usuario:
{prompt}

Respuesta:"""

            response = ollama.generate(
                model=self.model,
                prompt=full_prompt
            )

            return response['response']

        except Exception as e:
            return f"❌ Error al generar respuesta: {str(e)}"

    def interpret_statistics(self, statistics: Dict[str, Any], variable_name: str) -> str:
        """
        Interpreta estadísticas descriptivas

        Args:
            statistics: Diccionario con estadísticas
            variable_name: Nombre de la variable

        Returns:
            Interpretación en lenguaje natural
        """
        context = f"""
Variable analizada: {variable_name}

Estadísticas:
- Media: {statistics.get('mean', 'N/A')}
- Mediana: {statistics.get('50%', 'N/A')}
- Desviación estándar: {statistics.get('std', 'N/A')}
- Mínimo: {statistics.get('min', 'N/A')}
- Máximo: {statistics.get('max', 'N/A')}
- Asimetría (skewness): {statistics.get('skewness', 'N/A')}
- Curtosis: {statistics.get('kurtosis', 'N/A')}
"""

        prompt = f"Interpreta estas estadísticas descriptivas de forma práctica para un farmacéutico. " \
                 f"¿Qué nos dicen estos números sobre {variable_name}? ¿Hay algo destacable?"

        return self.generate_response(prompt, context)

    def interpret_correlation(self, corr_matrix: pd.DataFrame, threshold: float = 0.5) -> str:
        """
        Interpreta matriz de correlación

        Args:
            corr_matrix: Matriz de correlación
            threshold: Umbral para correlaciones significativas

        Returns:
            Interpretación de correlaciones
        """
        # Encontrar correlaciones fuertes
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_corrs.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value
                    })

        context = f"""
Correlaciones encontradas (|r| >= {threshold}):
"""
        for corr in strong_corrs:
            context += f"\n- {corr['var1']} <-> {corr['var2']}: {corr['correlation']:.3f}"

        if not strong_corrs:
            context += "\nNo se encontraron correlaciones fuertes."

        prompt = "Interpreta estas correlaciones en el contexto farmacéutico. " \
                 "¿Qué relaciones son importantes? ¿Qué implicaciones tienen?"

        return self.generate_response(prompt, context)

    def interpret_test_results(self, test_type: str, results: Dict[str, Any]) -> str:
        """
        Interpreta resultados de pruebas estadísticas

        Args:
            test_type: Tipo de prueba ('t_test', 'anova', 'chi_square', etc.)
            results: Diccionario con resultados

        Returns:
            Interpretación del test
        """
        context = f"""
Prueba realizada: {test_type}

Resultados:
{json.dumps(results, indent=2, default=str)}
"""

        prompt = f"Explica estos resultados de {test_type} de forma clara. " \
                 f"¿Qué conclusiones podemos sacar? ¿Son los resultados significativos?"

        return self.generate_response(prompt, context)

    def suggest_analysis(self, data_summary: Dict[str, Any], objective: str) -> str:
        """
        Sugiere análisis apropiados según el objetivo

        Args:
            data_summary: Resumen de los datos
            objective: Objetivo del análisis

        Returns:
            Sugerencias de análisis
        """
        context = f"""
Resumen de los datos:
- Número de filas: {data_summary.get('n_rows', 'N/A')}
- Número de columnas: {data_summary.get('n_columns', 'N/A')}
- Columnas disponibles: {', '.join(data_summary.get('columns', []))}
- Tipos de variables: {data_summary.get('variable_types', {})}

Objetivo del usuario: {objective}
"""

        prompt = "¿Qué análisis estadísticos recomiendas para este objetivo? " \
                 "Sugiere análisis específicos y justifica por qué son apropiados."

        return self.generate_response(prompt, context)

    def explain_concept(self, concept: str) -> str:
        """
        Explica un concepto estadístico

        Args:
            concept: Concepto a explicar

        Returns:
            Explicación del concepto
        """
        prompt = f"Explica el concepto de '{concept}' en el contexto del análisis de datos farmacéuticos. " \
                 f"Usa un lenguaje claro y proporciona un ejemplo práctico si es posible."

        return self.generate_response(prompt, "")

    def generate_insights(self, df: pd.DataFrame, analysis_results: Dict[str, Any]) -> str:
        """
        Genera insights y recomendaciones basados en los análisis

        Args:
            df: DataFrame con los datos
            analysis_results: Resultados de análisis realizados

        Returns:
            Insights y recomendaciones
        """
        context = f"""
Datos analizados:
- Tamaño del dataset: {len(df)} filas x {len(df.columns)} columnas
- Variables: {', '.join(df.columns.tolist())}

Resultados de análisis:
{json.dumps(analysis_results, indent=2, default=str)}
"""

        prompt = "Basándote en estos datos y análisis, genera insights clave y recomendaciones prácticas " \
                 "para el farmacéutico. ¿Qué decisiones pueden tomar con esta información?"

        return self.generate_response(prompt, context)

    def help_with_error(self, error_message: str, context: str = "") -> str:
        """
        Ayuda a resolver errores

        Args:
            error_message: Mensaje de error
            context: Contexto del error

        Returns:
            Ayuda para resolver el error
        """
        prompt = f"He encontrado este error: '{error_message}'. " \
                 f"¿Qué significa y cómo puedo resolverlo? Contexto: {context}"

        return self.generate_response(prompt, "")

    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Chat conversacional con el asistente

        Args:
            user_message: Mensaje del usuario
            conversation_history: Historial de conversación

        Returns:
            Respuesta del asistente
        """
        if conversation_history:
            context = "Historial de conversación:\n"
            for msg in conversation_history[-5:]:  # Últimos 5 mensajes
                context += f"{msg['role']}: {msg['content']}\n"
        else:
            context = ""

        return self.generate_response(user_message, context)
