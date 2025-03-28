from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

app = Flask(__name__)

# Data training untuk model
data = {
    'Jakarta': {'slope': 8.5, 'intercept': 500},
    'Bandung': {'slope': 7.8, 'intercept': 450},
    'Tangerang': {'slope': 7.2, 'intercept': 400}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        luas_tanah = float(request.form['luas_tanah'])
        lokasi = request.form['lokasi']
        
        if lokasi not in data:
            return jsonify({'error': 'Lokasi tidak valid'})
        
        # Menghitung prediksi menggunakan persamaan linear
        slope = data[lokasi]['slope']
        intercept = data[lokasi]['intercept']
        prediksi = (slope * luas_tanah) + intercept
        
        return jsonify({
            'prediksi': f"Rp {prediksi:.2f} juta",
            'luas_tanah': luas_tanah,
            'lokasi': lokasi
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
