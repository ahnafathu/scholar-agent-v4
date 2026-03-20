# 🎓 Scholar AI Agent v4.0

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_svg)](https://scholar-agent-v4-2n2tmotwqpzqbcd3isyhtm.streamlit.app/)

Scholar AI Agent adalah alat pencarian beasiswa cerdas berbasis AI yang dirancang untuk membantu calon mahasiswa menemukan peluang studi di luar negeri secara efisien. Alat ini menggabungkan kekuatan **Google Gemini 1.5** dan **Real-time Web Scraping** untuk memberikan analisis peluang yang objektif.

---

## 🚀 Info 1: Kegunaan & Fungsi Utama

Aplikasi ini dirancang untuk memotong kebingungan saat mencari beasiswa dengan fitur:
* **Analisis Profil Akademik**: Mengevaluasi skor IELTS dan GPA/IPK Anda terhadap standar beasiswa internasional.
* **Hybrid Data Fetching**: Menarik data terbaru dari internet melalui web scraping dan menggabungkannya dengan basis data internal model AI.
* **Sistem Fallback**: Jika pencarian web terhambat (rate limited), sistem secara otomatis beralih ke database internal agar Anda tetap mendapatkan informasi.
* **Visualisasi Reliabilitas**: Menampilkan *Confidence Score* untuk menunjukkan seberapa akurat analisis AI terhadap data yang ditemukan.

---

## 🛠️ Info 2: Panduan Instalasi & Penggunaan Detail

### 1. Dapatkan API Key Gemini (Gratis)
Aplikasi ini membutuhkan akses ke model AI Google.
* Pergi ke [Google AI Studio](https://aistudio.google.com/).
* Login dengan akun Google Anda.
* Klik **"Get API key"** dan buat kunci baru.
* Simpan kunci ini dengan aman.

### 2. Setup Lokal (Terminal/CMD)
Jalankan perintah berikut di folder proyek Anda:
```bash
# Clone repository
git clone [https://github.com/ahnafathu/scholar-agent-v4.git](https://github.com/ahnafathu/scholar-agent-v4.git)
cd scholar-agent-v4

# Install semua library yang dibutuhkan
pip install -r requirements.txt


3. Konfigurasi Secrets (Keamanan Data)
Buat folder .streamlit dan file secrets.toml di dalamnya untuk menyimpan API Key secara privat:

Bash
mkdir .streamlit
# Isi file .streamlit/secrets.toml dengan format:
# API_KEY = "MASUKKAN_API_KEY_ANDA_DISINI"
Catatan: File ini sudah masuk dalam .gitignore sehingga tidak akan ter-upload ke GitHub publik Anda.

4. Menjalankan Aplikasi
Bash
streamlit run scholar_web.py
🌐 Info 3: Demo & Akses Publik
Anda bisa langsung mencoba aplikasi ini tanpa instalasi melalui tautan berikut:

👉 Live Demo: Scholar AI Agent v4.0

🧰 Tech Stack
Bahasa Pemrograman: Python 3.10+

AI Model: Google Gemini 1.5 Series

Interface: Streamlit Framework

Data Scraping: DuckDuckGo Search API & BeautifulSoup4

Engineered by Ahnaf | v4.0
