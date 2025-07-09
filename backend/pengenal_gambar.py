import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# 1. Muat model pre-trained MobileNetV2
# 'weights="imagenet"' berarti kita menggunakan pengetahuan dari dataset ImageNet.
print("Memuat model MobileNetV2...")
model = MobileNetV2(weights='imagenet')
print("Model berhasil dimuat!")

def prediksi_gambar(path_gambar):
    """
    Fungsi untuk mengambil path gambar, memprosesnya, dan mengembalikan prediksi.
    """
    try:
        
        img = image.load_img(path_gambar, target_size=(224, 224))

        img_array = image.img_to_array(img)
        
        img_array_expanded = np.expand_dims(img_array, axis=0)

        processed_img = preprocess_input(img_array_expanded)

        # 5. Lakukan prediksi
        predictions = model.predict(processed_img)

        # 6. "Terjemahkan" hasil prediksi menjadi teks yang bisa dibaca manusia
        # Kita ambil 3 prediksi teratas.
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        return decoded_predictions

    except FileNotFoundError:
        return "Error: File tidak ditemukan di path tersebut."
    except Exception as e:
        return f"Error: Terjadi kesalahan saat memproses gambar - {e}"

# Bagian utama program yang akan berjalan
if __name__ == "__main__":
    # Minta pengguna memasukkan path gambar
    path_input = input("Masukkan path lengkap ke gambar Anda: ")

    # Panggil fungsi prediksi
    hasil_prediksi = prediksi_gambar(path_input)

    # Tampilkan hasilnya
    print("\n--- Hasil Prediksi ---")
    if isinstance(hasil_prediksi, list):
        for i, (imagenet_id, label, score) in enumerate(hasil_prediksi):
            # 'label' adalah nama objeknya, 'score' adalah tingkat kepercayaan
            print(f"{i+1}. Objek: {label.replace('_', ' ')} (Kepercayaan: {score:.2%})")
    else:
        # Tampilkan pesan error jika ada masalah
        print(hasil_prediksi)
    print("----------------------\n")