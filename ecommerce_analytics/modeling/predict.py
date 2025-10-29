import pandas as pd
import numpy as np
from datetime import timedelta
from scipy.stats import boxcox
import joblib
import os
import json

from Ecommerce_Analytics.utils.paths import models_dir

def predict_customer_segment(rfm_df: pd.DataFrame) -> np.ndarray:
    """
    Predice el segmento de cliente para un DataFrame de RFM dado.
    
    Args:
        rfm_df (pd.DataFrame): DataFrame con columnas 'recency', 'frequency', 'monetary_value'.

    Returns:
        np.ndarray: Un array con el número de cluster predicho para cada cliente.
    """
    print("Iniciando predicción de segmento...")

    # --- 1. Carga de Artefactos ---
    models_path = models_dir()
    
    # Cargar modelo, escalador y lambdas
    try:
        kmeans_model = joblib.load(os.path.join(models_path, 'kmeans_model.pkl'))
        rfm_scaler = joblib.load(os.path.join(models_path, 'rfm_scaler.pkl'))
        with open(os.path.join(models_path, 'boxcox_lambdas.json'), 'r') as f:
            lambdas = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: No se encontró un artefacto del modelo. {e}")
        print("Por favor, ejecute el script de entrenamiento primero.")
        return None
        
    print("Artefactos del modelo cargados.")

    # --- 2. Preprocesamiento de Nuevos Datos ---
    # Asegurarse de que el DataFrame de entrada tiene las columnas necesarias
    required_cols = {'recency', 'frequency', 'monetary_value'}
    if not required_cols.issubset(rfm_df.columns):
        raise ValueError(f"El DataFrame de entrada debe contener las columnas: {required_cols}")

    # Aplicar la misma transformación Box-Cox con las lambdas guardadas
    rfm_df_processed = rfm_df.copy()
    rfm_df_processed['recency_boxcox'] = boxcox(rfm_df_processed['recency'], lmbda=lambdas['lambda_recency'])
    rfm_df_processed['frequency_boxcox'] = boxcox(rfm_df_processed['frequency'], lmbda=lambdas['lambda_frequency'])
    rfm_df_processed['monetary_value_boxcox'] = boxcox(rfm_df_processed['monetary_value'], lmbda=lambdas['lambda_monetary'])

    # Aplicar el mismo escalado
    features_to_scale = ["recency_boxcox", "frequency_boxcox", "monetary_value_boxcox"]
    rfm_scaled = rfm_scaler.transform(rfm_df_processed[features_to_scale])
    
    print("Preprocesamiento de nuevos datos completado.")

    # --- 3. Predicción ---
    predictions = kmeans_model.predict(rfm_scaled)
    
    print("Predicción completada.")
    return predictions

if __name__ == '__main__':
    # --- Ejemplo de uso ---
    # Crear un DataFrame de ejemplo con datos de clientes para predecir
    sample_customers = pd.DataFrame({
        'customer_id': [1, 2, 3],
        'recency': [15, 100, 150],          # Un cliente reciente, uno en riesgo, uno perdido
        'frequency': [8, 3, 1],             # Un cliente frecuente, uno moderado, uno ocasional
        'monetary_value': [25000, 7000, 500] # Un cliente de alto valor, uno medio, uno bajo
    })
    
    print("--- Ejecutando ejemplo de predicción ---")
    
    # Obtener las predicciones
    predicted_clusters = predict_customer_segment(sample_customers)

    if predicted_clusters is not None:
        sample_customers['predicted_cluster'] = predicted_clusters
        print("\nResultados de la predicción de ejemplo:")
        print(sample_customers)
        print("\nRecordatorio de clusters (basado en el análisis del notebook):")
        print("* Cluster 1: Campeones (Recencia baja, Frecuencia/Valor altos)")
        print("* Cluster 0: En Riesgo (Recencia media, Frecuencia/Valor medios)")
        print("* Cluster 2: Ocasionales/Perdidos (Recencia alta, Frecuencia/Valor bajos)")