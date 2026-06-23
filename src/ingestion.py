import os
import pandas as pd
from sqlalchemy import create_engine

# Database Connection
DATABASE_URL = "postgresql://tripplancaster@localhost:5432/dataco_supply_chain"
def run_ingestion():
    print("Starting the DataCo Ingestion Pipeline...")
    
    csv_path = os.path.join("data", "DataCoSupplyChainDataset.csv")
    if not os.path.exists(csv_path):
        print(f" Error: Could not find the dataset at {csv_path}. Make sure the CS file is placed inside your local 'data/' directory.")
        return
    
    engine = create_engine(DATABASE_URL)
    
    print("Reading raw data file...")
    df = pd.read_csv(csv_path, encoding="latin1")
    print(f"Successfully loaded {len(df)} raw rows.")
    
    print("Extracting and cleaning 'customers' data...")
    customers_df = df[[
        'Customer Id', 'Customer Fname', 'Customer Lname', 
        'Customer City', 'Customer State', 'Customer Zipcode', 'Customer Street'
    ]].copy()
    customers_df.columns = [
        'customer_id', 'customer_fname', 'customer_lname', 
        'customer_city', 'customer_state', 'customer_zipcode', 'customer_street'
    ]
    customers_df = customers_df.drop_duplicates(subset=['customer_id'])
    customers_df.to_sql('customers', engine, if_exists='append', index=False)
    print(f"Stored {len(customers_df)} unique customer records.")
    
    print("Extracting 'categories' data...")
    categories_df = df[['Category Id', 'Category Name']].copy()
    categories_df.columns = ['category_id', 'category_name']
    categories_df = categories_df.drop_duplicates(subset=['category_id'])
    categories_df.to_sql('categories', engine, if_exists='append', index=False)
    print(f"Stored {len(categories_df)} unique product categories.")
    
    print("Extracting 'products' data...")
    products_df = df[['Product Card Id', 'Product Name', 'Category Id', 'Product Price']].copy()
    products_df.columns = ['product_card_id', 'product_name', 'category_id', 'product_price']
    products_df = products_df.drop_duplicates(subset=['product_card_id'])
    products_df.to_sql('products', engine, if_exists='append', index=False)
    print(f"Stored {len(products_df)} unique product items.")
    
    print("Extracting 'orders' data...")
    orders_df = df[[
        'Order Id', 'Customer Id', 'order date (DateOrders)', 
        'Order Status', 'Shipping Mode', 'Market', 'Order Region'
    ]].copy()
    orders_df.columns = [
        'order_id', 'customer_id', 'order_date_dateorders', 
        'order_status', 'shipping_mode', 'market', 'order_region'
    ]
    
    orders_df['order_date_dateorders'] = pd.to_datetime(orders_df['order_date_dateorders'])
    orders_df = orders_df.drop_duplicates(subset=['order_id'])
    orders_df.to_sql('orders', engine, if_exists='append', index=False)
    print(f" Stored {len(orders_df)} unique orders.")
    
    print("Extracting 'order_items' data...")
    order_items_df = df[[
        'Order Item Id', 'Order Id', 'Product Card Id', 
        'Order Item Quantity', 'Order Item Product Price', 'Order Item Discount', 'Order Item Total'
    ]].copy()
    order_items_df.columns = [
        'order_item_id', 'order_id', 'product_card_id', 
        'order_item_quantity', 'order_item_product_price', 'order_item_discount', 'order_item_total'
    ]
    order_items_df = order_items_df.drop_duplicates(subset=['order_item_id'])
    order_items_df.to_sql('order_items', engine, if_exists='append', index=False)
    print(f"Stored {len(order_items_df)} unique order line-items.")
    
    print("Extracting 'fulfillment' data for ML features...")
    fulfillment_df = df[[
        'Order Id', 'Days for shipping (real)', 'Days for shipment (scheduled)', 
        'Delivery Status', 'Late_delivery_risk'
    ]].copy()
    fulfillment_df.columns = [
        'order_id', 'days_for_shipping_real', 'days_for_shipment_scheduled', 
        'delivery_status', 'late_delivery_risk'
    ]
    fulfillment_df = fulfillment_df.drop_duplicates(subset=['order_id'])
    fulfillment_df.to_sql('fulfillment', engine, if_exists='append', index=False)
    print(f"Stored {len(fulfillment_df)} unique fulfillment tracking rows.")
    
    print("\nThe local PostgreSQL database is fully populated and optimized!")
    
if __name__ == "__main__":
    run_ingestion()