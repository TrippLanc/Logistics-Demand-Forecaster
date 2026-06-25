import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://tripplancaster@localhost:5432/dataco_supply_chain"

def extract_and_engineer_features():
    engine = create_engine(DATABASE_URL)
    
    query = """
    SELECT 
        f.days_for_shipping_real, f.days_for_shipment_scheduled, f.delivery_status, f.late_delivery_risk,
        o.shipping_mode, o.market, o.order_region, o.order_date_dateorders,
        oi.order_item_quantity, oi.order_item_total, p.product_price, p.category_id
    FROM fulfillment f
    INNER JOIN orders o ON f.order_id = o.order_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_card_id = p.product_card_id;
    """
    
    df = pd.read_sql_query(query, con=engine)
    
    df['order_date_dateorders'] = pd.to_datetime(df['order_date_dateorders'])
    df['order_year'] = df['order_date_dateorders'].dt.year
    df['order_month'] = df['order_date_dateorders'].dt.month
    df['order_day'] = df['order_date_dateorders'].dt.day
    df['order_hour'] = df['order_date_dateorders'].dt.hour
    df['order_day_of_week'] = df['order_date_dateorders'].dt.dayofweek
    
    df_cleaned = df.drop(columns=['order_date_dateorders', 'delivery_status', 'days_for_shipping_real'])
    
    categorical_cols = ['shipping_mode', 'market', 'order_region']
    df_encoded = pd.get_dummies(df_cleaned, columns=categorical_cols, drop_first=True, dtype=int)
    
    return df_encoded

if __name__ == "__main__":
    df = extract_and_engineer_features()
    print(f"Feature engineering pipeline complete. Matrix shape: {df.shape}")