import pandas as pd
import numpy as np
from datetime import timedelta
from scipy.stats import boxcox
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib
import os
import json
from Ecommerce_Analytics.utils.paths import data_processed_dir, models_dir

def train_customer_segmentation_model():
    """
    Carga los datos de ventas, calcula RFM, entrena un modelo K-Means 
    y guarda los artefactos del modelo (modelo, escalador y lambdas).
    """
    print("Iniciando el entrenamiento del modelo de segmentación...")

    # --- 1. Carga de datos ---
    processed_sales_path = data_processed_dir("sale.csv")
    sales_df = pd.read_csv(processed_sales_path, encoding="utf-8")
    sales_df = sales_df[sales_df["customer_id"] != -1]
    sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"])
    sales_df["total_sale"] = sales_df["quantity"] * sales_df["sale"]
    
    print(f"Datos cargados. {len(sales_df)} registros.")

    # --- 2. Cálculo de RFM ---
    snapshot_date = sales_df["sale_date"].max() + timedelta(days=1)
    rfm_df = sales_df.groupby("customer_id", as_index=False).agg({
        "sale_date": lambda date: (snapshot_date - date.max()).days,
        "invoice_no": "nunique",
        "total_sale": "sum"
    })
    rfm_df.rename(columns={
        "sale_date": "recency",
        "invoice_no": "frequency",
        "total_sale": "monetary_value"
    }, inplace=True)
    
    print("Cálculo de RFM completado.")

    # --- 3. Preprocesamiento y Transformación ---
    # Transformación Box-Cox para normalizar la distribución
    rfm_df['recency_boxcox'], lambda_recency = boxcox(rfm_df["recency"])
    rfm_df['frequency_boxcox'], lambda_frequency = boxcox(rfm_df["frequency"])
    rfm_df['monetary_value_boxcox'], lambda_monetary = boxcox(rfm_df["monetary_value"])

    # Guardar lambdas para usarlas en la predicción
    lambdas = {
        'lambda_recency': lambda_recency,
        'lambda_frequency': lambda_frequency,
        'lambda_monetary': lambda_monetary
    }

    # Escalado de características
    features_to_scale = ["recency_boxcox", "frequency_boxcox", "monetary_value_boxcox"]
    rfm_to_scale = rfm_df[features_to_scale]

    rfm_scaler = StandardScaler()
    rfm_scaled = rfm_scaler.fit_transform(rfm_to_scale)
    
    print("Preprocesamiento completado (Box-Cox y StandardScaler).")

    # --- 4. Entrenamiento del Modelo K-Means ---
    k = 3
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    
    print(f"Entrenamiento de K-Means con k={k} completado.")

    # --- 5. Guardado de Artefactos ---
    models_path = models_dir()
    os.makedirs(models_path, exist_ok=True)

    # Guardar modelo
    kmeans_model_path = os.path.join(models_path, 'kmeans_model.pkl')
    joblib.dump(kmeans, kmeans_model_path)

    # Guardar escalador
    scaler_path = os.path.join(models_path, 'rfm_scaler.pkl')
    joblib.dump(rfm_scaler, scaler_path)
    
    # Guardar lambdas
    lambdas_path = os.path.join(models_path, 'boxcox_lambdas.json')
    with open(lambdas_path, 'w') as f:
        json.dump(lambdas, f)

    print(f"Modelo guardado en: {kmeans_model_path}")
    print(f"Escalador guardado en: {scaler_path}")
    print(f"Lambdas guardadas en: {lambdas_path}")
    print("\nEntrenamiento finalizado exitosamente.")

if __name__ == '__main__':
    train_customer_segmentation_model()