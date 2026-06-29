import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Create dummy dataset if not exists for demonstration
def create_sample_dataset():
    data = {
        'url_len': [20, 100, 15, 80, 25, 120, 18, 95],
        'dot_count': [2, 5, 1, 4, 2, 6, 1, 5],
        'digit_count': [0, 20, 0, 15, 2, 30, 0, 25],
        'hyphen_count': [0, 3, 0, 5, 1, 4, 0, 2],
        'has_https': [1, 0, 1, 0, 1, 0, 1, 0],
        'has_ip': [0, 1, 0, 0, 0, 1, 0, 1],
        'has_at': [0, 1, 0, 1, 0, 1, 0, 0],
        'label': [0, 1, 0, 1, 0, 1, 0, 1] # 0: Safe, 1: Phishing
    }
    df = pd.DataFrame(data)
    if not os.path.exists('dataset'): os.makedirs('dataset')
    df.to_csv('dataset/phishing_dataset.csv', index=False)
    return df

def train():
    if not os.path.exists('dataset/phishing_dataset.csv'):
        df = create_sample_dataset()
    else:
        df = pd.read_csv('dataset/phishing_dataset.csv')

    X = df.drop('label', axis=1)
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    if not os.path.exists('model'): os.makedirs('model')
    joblib.dump(model, 'model/phishing_model.pkl')
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    train()