"""
Script para generar datos de ejemplo de farmacia
Ejecutar después de instalar las dependencias
"""
import pandas as pd
import numpy as np
from pathlib import Path

def generate_pharmacy_data(n_rows=500, output_file='data/examples/farmacia_ejemplo.csv'):
    """
    Genera datos sintéticos de farmacia para ejemplos y pruebas

    Args:
        n_rows: Número de filas a generar
        output_file: Ruta del archivo de salida
    """
    print(f"📊 Generando {n_rows} filas de datos de ejemplo...")

    np.random.seed(42)

    # Generar fechas
    dates = pd.date_range('2023-01-01', periods=n_rows, freq='D')

    # Generar datos base
    df = pd.DataFrame({
        'fecha': dates,
        'ventas_euros': np.random.normal(1500, 300, n_rows),
        'num_clientes': np.random.poisson(50, n_rows),
        'categoria': np.random.choice(['Medicamentos', 'Cosmetica', 'Higiene', 'Nutricion'], n_rows),
        'prescripcion': np.random.choice(['Si', 'No'], n_rows, p=[0.6, 0.4]),
        'satisfaccion': np.random.randint(1, 6, n_rows),
        'edad_promedio': np.random.normal(45, 15, n_rows).clip(18, 90),
        'temperatura': np.random.normal(20, 5, n_rows),
        'dia_semana': [d.strftime('%A') for d in dates],
        'mes': [d.strftime('%B') for d in dates],
        'trimestre': [(d.month - 1) // 3 + 1 for d in dates]
    })

    # Añadir correlaciones realistas
    # Ventas correlacionadas con número de clientes
    df['ventas_euros'] = df['ventas_euros'] + df['num_clientes'] * 10 + np.random.normal(0, 100, n_rows)
    df['ventas_euros'] = df['ventas_euros'].clip(lower=200)

    # Mayor satisfacción cuando hay menos tiempo de espera (inversamente proporcional a clientes)
    df['satisfaccion'] = np.where(
        df['num_clientes'] < 40,
        np.random.choice([4, 5], n_rows, p=[0.4, 0.6]),
        np.where(
            df['num_clientes'] < 55,
            np.random.choice([3, 4, 5], n_rows, p=[0.3, 0.4, 0.3]),
            np.random.choice([1, 2, 3], n_rows, p=[0.2, 0.5, 0.3])
        )
    )

    # Medicamentos con prescripción tienen mayor venta promedio
    df.loc[df['prescripcion'] == 'Si', 'ventas_euros'] *= 1.2

    # Redondear valores
    df['ventas_euros'] = df['ventas_euros'].round(2)
    df['edad_promedio'] = df['edad_promedio'].round(1)
    df['temperatura'] = df['temperatura'].round(1)

    # Crear directorio si no existe
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar
    df.to_csv(output_file, index=False)

    print(f"✅ Datos generados exitosamente!")
    print(f"   📁 Archivo: {output_file}")
    print(f"   📊 Filas: {len(df)}")
    print(f"   📋 Columnas: {len(df.columns)}")
    print(f"\nColumnas generadas:")
    for col in df.columns:
        print(f"   - {col} ({df[col].dtype})")

    print(f"\nEstadísticas básicas:")
    print(f"   💰 Ventas promedio: {df['ventas_euros'].mean():.2f}€")
    print(f"   👥 Clientes promedio: {df['num_clientes'].mean():.1f}")
    print(f"   ⭐ Satisfacción promedio: {df['satisfaccion'].mean():.2f}/5")

    return df

def generate_additional_datasets():
    """Genera datasets adicionales para casos de uso específicos"""

    # Dataset 2: Inventario de medicamentos
    print("\n📦 Generando dataset de inventario...")
    np.random.seed(43)
    n = 200

    df_inventory = pd.DataFrame({
        'codigo_producto': [f'MED{i:04d}' for i in range(1, n+1)],
        'nombre': [f'Medicamento {i}' for i in range(1, n+1)],
        'categoria': np.random.choice(['Analgésico', 'Antibiótico', 'Vitaminas', 'Antialérgico'], n),
        'stock_actual': np.random.randint(10, 500, n),
        'stock_minimo': np.random.randint(20, 100, n),
        'precio_venta': np.random.uniform(5, 150, n).round(2),
        'precio_coste': np.random.uniform(3, 100, n).round(2),
        'caducidad_dias': np.random.randint(30, 730, n),
        'proveedor': np.random.choice(['Proveedor A', 'Proveedor B', 'Proveedor C'], n),
        'prescripcion_requerida': np.random.choice(['Si', 'No'], n, p=[0.4, 0.6])
    })

    df_inventory.to_csv('data/examples/inventario_farmacia.csv', index=False)
    print(f"   ✅ Guardado: inventario_farmacia.csv")

    # Dataset 3: Satisfacción de clientes
    print("\n⭐ Generando dataset de satisfacción...")
    np.random.seed(44)
    n = 300

    df_satisfaction = pd.DataFrame({
        'fecha': pd.date_range('2023-01-01', periods=n, freq='D'),
        'satisfaccion_general': np.random.randint(1, 6, n),
        'tiempo_espera_min': np.random.randint(5, 45, n),
        'atencion_personal': np.random.randint(1, 6, n),
        'disponibilidad_producto': np.random.randint(1, 6, n),
        'limpieza_local': np.random.randint(3, 6, n),  # Generalmente alta
        'precio_percibido': np.random.randint(1, 6, n),
        'volveria': np.random.choice(['Si', 'No', 'Tal vez'], n, p=[0.7, 0.1, 0.2]),
        'edad_cliente': np.random.normal(50, 20, n).clip(18, 90).round(0),
        'genero': np.random.choice(['Masculino', 'Femenino', 'Otro'], n, p=[0.45, 0.52, 0.03])
    })

    # Correlación: menos tiempo de espera = mayor satisfacción
    df_satisfaction['satisfaccion_general'] = np.where(
        df_satisfaction['tiempo_espera_min'] < 15,
        np.random.choice([4, 5], n, p=[0.3, 0.7]),
        np.where(
            df_satisfaction['tiempo_espera_min'] < 30,
            np.random.choice([3, 4], n, p=[0.5, 0.5]),
            np.random.choice([1, 2, 3], n, p=[0.3, 0.4, 0.3])
        )
    )

    df_satisfaction.to_csv('data/examples/satisfaccion_clientes.csv', index=False)
    print(f"   ✅ Guardado: satisfaccion_clientes.csv")

    print("\n🎉 Todos los datasets de ejemplo generados!")

if __name__ == "__main__":
    print("=" * 60)
    print("Generador de Datos de Ejemplo - Sistema de Análisis Farmacéutico")
    print("=" * 60)
    print()

    # Dataset principal
    df = generate_pharmacy_data(n_rows=500)

    # Datasets adicionales
    try:
        generate_additional_datasets()
    except Exception as e:
        print(f"\n⚠️  Error al generar datasets adicionales: {e}")

    print("\n" + "=" * 60)
    print("✅ Proceso completado!")
    print("=" * 60)
