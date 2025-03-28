import sys
import locale
import warnings

warnings.filterwarnings('ignore')

# Set encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    pass

from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Data training untuk setiap kota (dummy data)
data = {
    'Jakarta': {
        'slope': 10,
        'intercept': 500
    },
    'Bandung': {
        'slope': 9,
        'intercept': 450
    },
    'Tangerang': {
        'slope': 8,
        'intercept': 400
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Mengambil input dari form
    luas_tanah = float(request.form['luas_tanah'])
    lokasi = request.form['lokasi']
    
    # Menghitung prediksi
    harga = data[lokasi]['slope'] * luas_tanah + data[lokasi]['intercept']
    
    # Membuat plot
    plt.figure(figsize=(10, 6))
    
    # Plot untuk setiap kota
    x = np.linspace(0, 500, 100)
    for kota in data.keys():
        y = data[kota]['slope'] * x + data[kota]['intercept']
        plt.plot(x, y, label=kota)
    
    # Plot titik prediksi
    plt.scatter(luas_tanah, harga, color='green', label='Prediksi Anda')
    
    plt.xlabel('Luas Tanah (m²)')
    plt.ylabel('Harga Rumah (Juta Rupiah)')
    plt.title('Hasil Prediksi')
    plt.legend()
    plt.grid(True)
    
    # Konversi plot ke base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return jsonify({
        'prediksi': f"Rp {harga:.2f} juta",
        'plot': plot_url
    })

if __name__ == '__main__':
    app.run(debug=True)
