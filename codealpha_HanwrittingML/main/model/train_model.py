import os
import gzip
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import urllib.request

# --- CONFIGURATION ---
DATA_DIR = './data'
MODEL_NAME = 'char_model.h5'

def download_mnist():
    """Downloads the MNIST dataset files into the project folder."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    base_url = 'https://storage.googleapis.com/cvdf-datasets/mnist/'
    files = [
        'train-images-idx3-ubyte.gz', 'train-labels-idx1-ubyte.gz',
        't10k-images-idx3-ubyte.gz', 't10k-labels-idx1-ubyte.gz'
    ]
    
    for file in files:
        path = os.path.join(DATA_DIR, file)
        if not os.path.exists(path):
            print(f"Downloading {file}...")
            urllib.request.urlretrieve(base_url + file, path)
    print("Dataset files are now in the /data folder.")

def load_local_data():
    """Extracts and loads the raw bytes from the local /data folder."""
    def extract_images(path):
        with gzip.open(path, 'rb') as f:
            # Skip the 16-byte header
            return np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28, 28, 1)

    def extract_labels(path):
        with gzip.open(path, 'rb') as f:
            # Skip the 8-byte header
            return np.frombuffer(f.read(), np.uint8, offset=8)

    x_train = extract_images(os.path.join(DATA_DIR, 'train-images-idx3-ubyte.gz'))
    y_train = extract_labels(os.path.join(DATA_DIR, 'train-labels-idx1-ubyte.gz'))
    x_test = extract_images(os.path.join(DATA_DIR, 't10k-images-idx3-ubyte.gz'))
    y_test = extract_labels(os.path.join(DATA_DIR, 't10k-labels-idx1-ubyte.gz'))
    
    return (x_train / 255.0), y_train, (x_test / 255.0), y_test

def run_training():
    download_mnist()
    x_train, y_train, x_test, y_test = load_local_data()
    
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    print("Starting Training...")
    model.fit(x_train, y_train, epochs=3, batch_size=64)
    model.save(MODEL_NAME)
    print(f"Model saved as {MODEL_NAME}")

if __name__ == "__main__":
    run_training()