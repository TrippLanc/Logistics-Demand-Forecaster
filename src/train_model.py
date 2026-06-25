import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from features import extract_and_engineer_features

def train_and_save_model():
    print("Running feature engineering pipeline...")
    df = extract_and_engineer_features()
    
    X = df.drop(columns=['late_delivery_risk'])
    y = df['late_delivery_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("🏋️ Training production Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model training complete. Test Accuracy: {acc * 100:.2f}%")
    
    os.makedirs('models', exist_ok=True)
    artifacts = {'model': model, 'features': list(X.columns)}
    
    model_path = os.path.join('models', 'late_delivery_rf_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(artifacts, f)
    print(f"Production model artifacts saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()