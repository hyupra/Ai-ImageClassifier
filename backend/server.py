# File: backend/server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# Impor fungsi prediksi dari script logika AI kita
from pengenal_gambar import prediksi_gambar 

app = Flask(__name__)
# CORS (Cross-Origin Resource Sharing) penting agar frontend bisa mengakses server ini
CORS(app) 

# Konfigurasi folder untuk menyimpan gambar yang diunggah sementara
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Definisikan endpoint API untuk prediksi
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang dikirim'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Panggil fungsi AI untuk melakukan prediksi
        hasil_prediksi = prediksi_gambar(filepath)

        if isinstance(hasil_prediksi, list):
            # Format hasil agar mudah dibaca oleh frontend (dalam format JSON)
            formatted_result = [{'label': label.replace('_', ' '), 'score': float(score)} for _, label, score in hasil_prediksi]
            return jsonify(formatted_result)
        else:
            # Jika terjadi error di fungsi prediksi
            return jsonify({'error': str(hasil_prediksi)}), 500

if __name__ == '__main__':
    # Jalankan server di semua alamat IP yang tersedia di port 5000
    app.run(host='0.0.0.0', port=5000)