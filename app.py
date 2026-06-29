from flask import Flask, render_to_directory, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import joblib
import numpy as np
from utils.feature_extractor import extract_features
import os

app = Flask(__name__)
app.secret_key = "phishing_secret_key"

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/phishing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class DetectionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    result = db.Column(db.String(50))
    confidence = db.Column(db.Float)

# Create DB folders
if not os.path.exists('database'): os.makedirs('database')

# Load Model
model = joblib.load('model/phishing_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    url = request.form.get('url')
    features = np.array(extract_features(url)).reshape(1, -1)
    
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    confidence = round(np.max(probability) * 100, 2)
    
    result = "Phishing" if prediction == 1 else "Safe"
    
    # Save to history
    new_entry = DetectionHistory(url=url, result=result, confidence=confidence)
    db.session.add(new_entry)
    db.session.commit()
    
    return render_template('result.html', url=url, result=result, confidence=confidence)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        flash('Invalid Credentials')
    return render_template('login.html')

@app.route('/admin/dashboard')
def dashboard():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    history = DetectionHistory.query.all()
    total_safe = DetectionHistory.query.filter_by(result='Safe').count()
    total_phish = DetectionHistory.query.filter_by(result='Phishing').count()
    
    return render_template('dashboard.html', history=history, safe=total_safe, phish=total_phish)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)