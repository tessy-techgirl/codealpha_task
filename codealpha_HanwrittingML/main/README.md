# InkLogic : Handwritten Character Recognition System

InkLogic  is a full-stack web application designed for high-accuracy handwritten character recognition. Built as a final-year research project, it leverages deep learning to bridge the gap between physical handwriting and digital text.

## 🚀 Features
- **CNN-Powered Inference**: Uses a Convolutional Neural Network (TensorFlow/Keras) for character classification.
- **Secure Authentication**: Built-in login/registration system with password hashing.
- **Modern UI**: A clean, Charcoal & Emerald-themed dashboard for seamless user interaction.
- **Log Analytics**: Stores prediction history in a MySQL database for performance tracking.

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, Modern CSS, JavaScript (ES6+)
- **AI/ML**: TensorFlow, Keras, NumPy, Pillow
- **Database**: MySQL (Workbench/XAMPP)

## 📂 Setup Instructions
1. Import `database.sql` into your MySQL instance.
2. Install dependencies: `pip install flask tensorflow mysql-connector-python pillow`
3. Run the application: `python app.py`
4. Access via `http://127.0.0.1:8080/login`