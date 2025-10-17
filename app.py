from flask import Flask, request, render_template, redirect, url_for, session, jsonify, flash
import json
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load trained model
MODEL_PATH = "Xception_model.h5"  # Update if needed
model = load_model(MODEL_PATH)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess_image(img_path, target_size=(224, 224)):
    """Load and preprocess image for prediction"""
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

USER_FILE = 'users.json'

def load_users():
    try:
        with open(USER_FILE, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        number = request.form['number']
        address = request.form['address']
        
        if username in users:
            flash('User already exists! Please log in.', 'danger')
            return redirect(url_for('login'))

        users[username] = {
            'email': email,
            'password': generate_password_hash(password),
            'number': number,
            'address': address
        }
        save_users(users)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route("/index", methods=["GET", "POST"])
def index():
    prediction = None
    uploaded_file = None
    confidence = 0
    reason = ""

    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", prediction="No file uploaded")

        file = request.files["file"]

        if file.filename == "":
            return render_template("index.html", prediction="No file selected")

        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)  # Save the file
            
            img_array = preprocess_image(file_path)  # Preprocess the image
            pred_prob = model.predict(img_array)[0][0]  # Get prediction probability
            
            # Threshold-based classification (Adjust based on dataset)
            if pred_prob < 0.5:
                prediction = "FAKE"
                confidence = pred_prob * 100
                reason = "Fake images often have digital artifacts, blurriness, or unnatural lighting."
            else:
                prediction = "REAL"
                confidence = (1 - pred_prob) * 100
                reason = "Real images have natural textures, proper lighting, and consistent colors."

            return render_template("index.html", prediction=prediction, file_path=file_path, confidence=round(confidence, 2), reason=reason)

    return render_template("index.html", prediction=prediction, file_path=None, confidence=confidence, reason=reason)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
