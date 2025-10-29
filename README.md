# 🛍️ Ecommerce Analytics: Customer Segmentation & Sales Forecasting

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python 3.10">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue.svg" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Dashboard-Power_BI-yellow.svg" alt="Power BI">
  <img src="https://img.shields.io/badge/Status-Completed-green.svg" alt="Status">
</p>

---

## 🎯 Project Overview

This project provides a comprehensive analysis of an e-commerce dataset with two primary objectives:

1.  **Customer Segmentation:** To identify distinct customer groups based on their purchasing behavior. This is achieved by calculating **Recency, Frequency, and Monetary (RFM)** metrics and applying clustering algorithms to segment customers into meaningful categories such as "Champions," "At-Risk," and "Occasional."
2.  **Sales Forecasting:** To analyze historical sales data to understand trends, seasonality, and stationarity, laying the groundwork for future sales prediction models.

The project is structured to separate exploratory analysis (in Jupyter Notebooks) from operational code (in Python scripts), making it modular, reproducible, and ready for production environments.

---

## 🛠️ Core Technologies

This project is built upon a modern data stack:

*   **Database:** **PostgreSQL** is used as the primary data source for storing transactional and customer data.
*   **Backend & Analysis:** **Python 3.10** is the core language for data processing, analysis, and machine learning. Key libraries include:
    *   `pandas` & `numpy`: For data manipulation.
    *   `scikit-learn`: For machine learning (K-Means, StandardScaler, PCA).
    *   `scipy`: For statistical transformations (Box-Cox).
    *   `SQLAlchemy`: To connect and interact with the PostgreSQL database.
    *   `joblib`: For model persistence.
*   **Visualization & Dashboarding:** **Power BI** is used to create an interactive dashboard for visualizing key metrics and segment characteristics. Python libraries like `matplotlib`, `seaborn`, and `plotly` are used for exploratory analysis.

---

## 📊 Dataset

The analysis is based on four key data files located in the `data/raw` directory, originally sourced from the PostgreSQL database:
*   `sale.csv`: Contains transactional data, including customer IDs, invoice numbers, product details, quantities, and prices.
*   `customer.csv`: Information about each customer.
*   `product.csv`: Details about each product.
*   `state.csv`: Geographic information related to sales.

---

## 🚀 Installation Guide

To set up the project environment, you can use either `conda` or `pip`. Please refer to [install.md](install.md) for more detailed instructions.

### Using Conda (Recommended)

1.  **Create the environment:**
    ```bash
    conda env create -f environment.yml
    ```

2.  **Activate the environment:**
    ```bash
    conda activate ecommerce_analytics
    ```

### Using Pip

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Pipelines

The project includes two main automated pipelines for model lifecycle management.

### 1. Training Pipeline (`train.py`)

This pipeline automates the process of creating and saving the segmentation model.
*   **Input:** `sale.csv` from the processed data folder.
*   **Process:**
    1.  Calculates RFM metrics for each customer.
    2.  Applies Box-Cox transformation and `StandardScaler` for data normalization.
    3.  Trains a K-Means clustering model (k=3).
*   **Output:** Saves three critical artifacts in the `/models` directory:
    *   `kmeans_model.pkl`: The trained clustering model.
    *   `rfm_scaler.pkl`: The scaler used for preprocessing.
    *   `boxcox_lambdas.json`: The lambda values from the Box-Cox transformation.

**To run the training pipeline:**
```bash
python -m Ecommerce_Analytics.modeling.train
```

### 2. Prediction Pipeline (`predict.py`)

This pipeline uses the trained model to classify new or existing customers into segments.
*   **Input:** A DataFrame containing customer RFM data.
*   **Process:**
    1.  Loads the saved model, scaler, and lambdas.
    2.  Applies the exact same preprocessing steps to the new data.
    3.  Predicts the cluster for each customer.
*   **Output:** Returns the predicted cluster labels.

**To run the example prediction:**
```bash
python -m Ecommerce_Analytics.modeling.predict
```

---

## 📈 Dashboard

A Power BI dashboard file (`dashboard/dashboard.pbix`) is included to provide a high-level, interactive view of the key business metrics and customer segments. It allows for easy exploration of sales trends, geographical distribution, and the characteristics of each customer cluster.

---

## 📂 Project Organization

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── install.md         <- Detailed instructions to set up this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description.
    │
    ├── environment.yml    <- The requirements file for reproducing the analysis environment.
    ├── requirements.txt   <- The pip requirements file for reproducing the environment.
    │
    ├── test               <- Unit and integration tests for the project.
    │
    ├── setup.py           <- Makes project pip installable (pip install -e .)
    │
    └── Ecommerce_Analytics   <- Source code for use in this project.
        │
        ├── __init__.py             <- Makes Ecommerce_Analytics a Python module.
        │
        ├── config.py               <- Stores useful variables and configuration.
        │
        ├── dataset.py              <- Scripts to download or generate data.
        │
        ├── modeling                
        │   ├── __init__.py 
        │   ├── predict.py          <- Code to run model inference with trained models.
        │   └── train.py            <- Code to train models.
        │
        ├── utils                   <- Scripts to help with common tasks.
        │   └── paths.py            <- Helper functions for relative file referencing.        
        │
        └── plot.py                <- Code to create visualizations.

---
Project based on the [cookiecutter conda data science project template](https://github.com/jvelezmagic/cookiecutter-conda-data-science).