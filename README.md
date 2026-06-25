# Logistics-Demand-Forecaster

This repository contains an end-to-end machine learning and data engineering pipeline designed to predict late delivery risks at the point of customer checkout. The project transitions raw supply chain data through a structured relational database, executes feature engineering to isolate predictive signals while eliminating data leakage, trains an ensemble tree classifier, and serves predictions through an interactive web interface.

## System Architecture

The project is structured to separate data ingestion, feature transformation, model training, and user deployment:

* **`database/schema.sql`**: Relational DDL script establishing the PostgreSQL schema, primary/foreign key relationships, and structural constraints.
* **`src/ingestion.py`**: Automated ETL script that reads the raw data, normalizes it into separate entity dataframes, and writes the records to PostgreSQL.
* **`src/features.py`**: Data extraction and transformation pipeline that handles time-series parsing, categorical encoding, and operational feature isolation.
* **`src/train_model.py`**: Production training script that splits historical datasets, handles class distributions, optimizes a Random Forest classifier, and serializes model artifacts.
* **`app/main.py`**: Interactive Streamlit web application allowing logistics operators to simulate order profiles and evaluate delivery risk instantly.

---

## Data Engineering & Pipeline Mechanics

### 1. Relational Database Modeling
The raw transaction records are normalized into a relational structure inside PostgreSQL to reduce redundancy and enforce data integrity. The ingestion pipeline populates six core tables:
* `customers`: Unique client profiles and geographic attributes.
* `categories`: Product classification hierarchy.
* `products`: Inventory items and baseline pricing.
* `orders`: Temporal checkout details and market routing data.
* `order_items`: Specific transaction line-item quantities and totals.
* `fulfillment`: Real-world transit metrics and scheduled requirements.

### 2. Eliminating Data Leakage
Initial model iterations achieved an artificial accuracy of 97.57% due to the inclusion of downstream fulfillment variables (`days_for_shipping_real` and a calculated delivery buffer). Because actual shipping duration cannot be known at the moment an order is placed, utilizing these variables introduced mathematical data leakage. 

To create a valid forward-looking forecasting system, these future features were removed from the training matrix. The final production model relies strictly on features available at checkout, achieving a true baseline predictive accuracy of 71.83%.

### 3. Core Feature Importance
The leak-free model relies heavily on three primary operational drivers to identify high-risk shipments:
* `days_for_shipment_scheduled`: The tight timeline constraints promised to the consumer.
* `shipping_mode_Standard Class`: The structural baseline priority tier assigned to the parcel.
* `order_hour`: The temporal cutoff window during which processing backlogs frequently occur.

---

## Installation & Deployment Guide

Follow these steps to run the complete pipeline locally on your machine.

### Prerequisites
* PostgreSQL running locally.
* Python 3.10 or higher.
* A clone of this repository.

### 1. Environment Setup
Navigate to the root directory, create a virtual environment, and install the required dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Database Initialization
Create a PostgreSQL database named `dataco_supply_chain` and apply the DDL schema file:

```bash
createdb dataco_supply_chain
psql -d dataco_supply_chain -f database/schema.sql
```

### 3. Execute the Ingestion Pipeline
Place the source CSV file inside the `data/` directory as `DataCoSupplyChainDataset.csv`, then run the ingestion script to populate the database:

```bash
python src/ingestion.py
```

### 4. Train the Production Model
Run the model training script to process the features from the database, execute the train/test split, and serialize the model artifacts to disk:

```bash
python src/train_model.py
```

### 5. Launch the Web Interface
Run the Streamlit application server to open the interactive forecasting dashboard in your browser:

```bash
streamlit run app/main.py
```
