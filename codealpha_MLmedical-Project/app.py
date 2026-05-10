from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
import pickle
import numpy as np
import os
from datetime import datetime

# Initialize Flask App FIRST
app = Flask(__name__)
app.secret_key = 'medcare_intern_secret'

# Health Tips Logic
HEALTH_ADVICE = {
    "diabetes": {
        "positive": "⚠️ High Risk: Consult an endocrinologist. Reduce sugar, increase fiber, and walk 30 mins daily.",
        "negative": "✅ Healthy: Your glucose levels look good. Maintain a balanced diet and stay active!"
    },
    "heart": {
        "positive": "⚠️ High Risk: Please see a cardiologist. Minimize salt intake and monitor blood pressure.",
        "negative": "✅ Healthy: Your heart indicators are strong. Keep up the cardio exercises!"
    },
    "cancer": {
        "positive": "⚠️ Urgent: Please schedule a professional screening/biopsy with an oncologist immediately.",
        "negative": "✅ Healthy: Screening is clear. Continue regular self-exams and a healthy diet."
    }
}

# Database Helper
def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="medical_system"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.form.get('username', 'Guest')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session: return redirect(url_for('index'))
    
    choice = request.form.get('disease_choice')
    
    try:
        # Get user inputs from the form
        # We ask for the basics and pad the rest for the model
        val1 = float(request.form.get('v1', 0))
        val2 = float(request.form.get('v2', 0))
        val3 = float(request.form.get('v3', 0))
        val4 = float(request.form.get('v4', 0))
        val5 = float(request.form.get('v5', 0))

        # Construct feature list based on which model is selected
        if choice == 'diabetes':
            # Model expects 8 features: [Preg, Glu, BP, Skin, Ins, BMI, Ped, Age]
            features = [val1, val2, val3, 20.0, 80.0, val4, 0.5, val5]
        elif choice == 'heart':
            # Model expects 13 features: [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            features = [val5, val1, val2, 120, 200, 0, 1, val3, val4, 1.0, 1, 0, 2]
        else: # cancer
            # Simplified for demo (Models usually need 30, we pad the rest)
            features = [val1, val2, val3, val4, val5] + [0.1]*25

        # Load Brain
        model = pickle.load(open(f'models/{choice}_model.pkl', 'rb'))
        scaler = pickle.load(open(f'models/{choice}_scaler.pkl', 'rb'))
        
        # Predict
        prediction = model.predict(scaler.transform([features]))[0]
        status = "positive" if prediction == 1 else "negative"
        result_text = "Action Required" if prediction == 1 else "Normal / Low Risk"
        advice = HEALTH_ADVICE[choice][status]

        # Save to MySQL
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO history (username, disease, result, date) VALUES (%s, %s, %s, %s)",
                       (session['user'], choice, result_text, datetime.now()))
        db.commit()

        return render_template('dashboard.html', prediction=result_text, advice=advice, status=status)

    except Exception as e:
        return render_template('dashboard.html', prediction=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=8080) # Changed port to 8080 to avoid Windows errors

# from flask import Flask, render_template, request, session, redirect
# import mysql.connector
# import pickle
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = 'internship_2026'

# # Helper for Database
# def get_db():
#     return mysql.connector.connect(
#         host="localhost", user="root", password="_T57ERESA-22F", database="medical_system"
#     )

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login', methods=['POST'])
# def login():
#     session['user'] = request.form['username']
#     return redirect('/dashboard')

# @app.route('/dashboard')
# def dashboard():
#     if 'user' not in session: return redirect('/')
#     return render_template('dashboard.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'user' not in session: return redirect('/')
    
#     choice = request.form['disease_choice']
#     symptom_string = request.form['symptoms']
    
#     # Convert comma-separated string to list of floats
#     try:
#         input_data = [float(x.strip()) for x in symptom_string.split(',')]
        
#         # Load the specific selected model and scaler
#         model = pickle.load(open(f'models/{choice}_model.pkl', 'rb'))
#         scaler = pickle.load(open(f'models/{choice}_scaler.pkl', 'rb'))
        
#         # Process and Predict
#         processed_data = scaler.transform([input_data])
#         prediction = model.predict(processed_data)
        
#         result = "Positive/High Risk" if prediction[0] == 1 else "Negative/Low Risk"
        
#         # Log to MySQL
#         db = get_db()
#         cursor = db.cursor()
#         cursor.execute("INSERT INTO model_results (patient_name, disease_type, algorithm, accuracy_score, date_tested) VALUES (%s, %s, %s, %s, %s)",
#                        (session['user'], choice, 'Random Forest', 0.85, datetime.now()))
#         db.commit()
        
#         return render_template('dashboard.html', prediction=result)
#     except Exception as e:
#         return render_template('dashboard.html', prediction=f"Error: Ensure you entered the correct number of values.")

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/')

# if __name__ == '__main__':
#     app.run(debug=True, port=8080)

# # import pandas as pd
# # import numpy as np
# # import mysql.connector
# # import os
# # from datetime import datetime

# # # ML Imports
# # from sklearn.model_selection import train_test_split
# # from sklearn.preprocessing import StandardScaler, LabelEncoder
# # from sklearn.linear_model import LogisticRegression
# # from sklearn.svm import SVC
# # from sklearn.ensemble import RandomForestClassifier
# # from xgboost import XGBClassifier
# # from sklearn.metrics import accuracy_score

# # # --- STAGE 1: MYSQL CONNECTION ---
# # def get_db_connection():
# #     return mysql.connector.connect(
# #         host="localhost",
# #         user="root",          # Default username for MySQL Workbench
# #         password="_T57ERESA-22F",          # ENTER YOUR PASSWORD HERE if you set one
# #         database="medical_system"
# #     )

# # def init_db():
# #     try:
# #         # First connect without database to create it if missing
# #         conn = mysql.connector.connect(host="localhost", user="root", password="_T57ERESA-22F")
# #         cursor = conn.cursor()
# #         cursor.execute("CREATE DATABASE IF NOT EXISTS medical_system")
# #         cursor.execute("USE medical_system")
        
# #         # Create the results table
# #         cursor.execute('''
# #             CREATE TABLE IF NOT EXISTS model_results (
# #                 id INT AUTO_INCREMENT PRIMARY KEY,
# #                 patient_name VARCHAR(255),
# #                 disease_type VARCHAR(100),
# #                 algorithm VARCHAR(100),
# #                 accuracy_score FLOAT,
# #                 date_tested DATETIME
# #             )
# #         ''')
# #         conn.commit()
# #         cursor.close()
# #         conn.close()
# #         print("MySQL Workbench: Database 'medical_system' is ready.")
# #     except mysql.connector.Error as err:
# #         print(f"Error: {err}")

# # # --- STAGE 2: LOGGING TO MYSQL ---
# # def log_to_mysql(name, disease, algo, acc):
# #     conn = get_db_connection()
# #     cursor = conn.cursor()
# #     sql = "INSERT INTO model_results (patient_name, disease_type, algorithm, accuracy_score, date_tested) VALUES (%s, %s, %s, %s, %s)"
# #     cursor.execute(sql, (name, disease, algo, acc, datetime.now()))
# #     conn.commit()
# #     cursor.close()
# #     conn.close()

# # # --- STAGE 3: MACHINE LEARNING ENGINE ---
# # def process_disease_task(file_path, target_col, disease_label):
# #     if not os.path.exists(file_path):
# #         print(f"File {file_path} not found.")
# #         return

# #     # Load and Preprocess
# #     df = pd.read_csv(file_path).dropna(axis=1, how='all')
# #     df = df.fillna(df.median(numeric_only=True))
    
# #     X = df.drop(columns=[target_col])
# #     y = df[target_col]
    
# #     if y.dtype == 'object':
# #         y = LabelEncoder().fit_transform(y)

# #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# #     scaler = StandardScaler()
# #     X_train = scaler.fit_transform(X_train)
# #     X_test = scaler.transform(X_test)

# #     # The 4 Required Algorithms
# #     models = {
# #         "Logistic Regression": LogisticRegression(),
# #         "SVM": SVC(probability=True),
# #         "Random Forest": RandomForestClassifier(),
# #         "XGBoost": XGBClassifier(eval_metric='logloss')
# #     }

# #     print(f"\n--- Results for {disease_label} ---")
# #     for name, model in models.items():
# #         model.fit(X_train, y_train)
# #         acc = accuracy_score(y_test, model.predict(X_test))
# #         print(f"{name}: {acc*100:.2f}%")
        
# #         # Log result into MySQL Workbench
# #         log_to_mysql("Nkwele Mboke Francine Teresa", disease_label, name, acc)

# # # --- STAGE 4: RUNTIME ---
# # if __name__ == "__main__":
# #     init_db()
    
# #     # Ensure your CSV files are in the 'data' folder
# #     tasks = [
# #         ("data/heart.csv", "target", "Heart Disease"),
# #         ("data/diabetes.csv", "Outcome", "Diabetes"),
# #         ("data/cancer.csv", "Class", "Breast Cancer")
# #     ]
    
# #     for path, target, label in tasks:
# #         process_disease_task(path, target, label)
    
# #     print("\n[SUCCESS] All results are now visible in MySQL Workbench.")
