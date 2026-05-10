import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import os

if not os.path.exists('models'): os.makedirs('models')

def train_and_save_all():
    # Configuration for your three files
    tasks = [
        ('data/diabetes.csv', 'Outcome', 'diabetes'),
        ('data/heart.csv', 'target', 'heartattack'),
        ('data/cancer.csv', 'Class', 'cancer')
    ]

    for file_path, target, name in tasks:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path).dropna()
            
            # Pre-processing
            X = df.drop(target, axis=1)
            y = df[target]
            
            # Handle Cancer labels (M/B) if they are strings
            if y.dtype == 'object':
                y = LabelEncoder().fit_transform(y)
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_scaled, y)
            
            # Save files
            pickle.dump(model, open(f'models/{name}_model.pkl', 'wb'))
            pickle.dump(scaler, open(f'models/{name}_scaler.pkl', 'wb'))
            print(f"✅ {name.capitalize()} model and scaler saved.")

if __name__ == "__main__":
    train_and_save_all()
# import pandas as pd
# import pickle
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# import os

# if not os.path.exists('models'): os.makedirs('models')

# def train_diabetes():
#     df = pd.read_csv('data/diabetes.csv')
#     X = df.drop('Outcome', axis=1)
#     y = df['Outcome']
    
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)
    
#     model = RandomForestClassifier(n_estimators=100)
#     model.fit(X_scaled, y)
    
#     # Save model and scaler
#     pickle.dump(model, open('models/diabetes_model.pkl', 'wb'))
#     pickle.dump(scaler, open('models/diabetes_scaler.pkl', 'wb'))
#     print("Diabetes Model Saved.")

# train_diabetes()