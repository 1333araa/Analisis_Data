# 🚲 Bike Sharing Analysis Dashboard

Proyek analisis data menggunakan **Bike Sharing Dataset** (Capital Bikeshare, Washington D.C., 2011–2012).

## 📋 Pertanyaan Bisnis
1. Bagaimana pengaruh kondisi cuaca dan musim terhadap jumlah penyewaan sepeda?
2. Bagaimana pola penyewaan berdasarkan jam dan hari dalam seminggu (pengguna kasual vs terdaftar)?
3. *(Analisis Lanjutan)* Bagaimana pengelompokan jam berdasarkan intensitas penggunaan?

## 📁 Struktur Proyek
```
submission/
├── dashboard/
│   ├── main_data.csv       # Data harian (sudah bersih)
│   └── dashboard.py        # Aplikasi Streamlit
├── data/
│   ├── day.csv             # Dataset harian mentah
│   └── hour.csv            # Dataset per-jam mentah
├── notebook.ipynb          # Notebook analisis lengkap
├── requirements.txt        # Dependensi Python
├── README.md               # File ini
└── url.txt                 # URL deployment Streamlit Cloud
```

## ⚙️ Cara Menjalankan Dashboard (Local)

### 1. Clone / ekstrak proyek
```bash
unzip submission.zip
cd submission
```

### 2. (Opsional) Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan dashboard
```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka di browser pada `http://localhost:8501`.

## 📊 Fitur Dashboard
- **Filter** berdasarkan tahun dan musim
- **KPI Metrics**: total penyewaan, rata-rata harian, kasual vs terdaftar
- **Tab 1 – Cuaca & Musim**: Boxplot, bar chart, scatter suhu
- **Tab 2 – Pola Jam & Hari**: Line chart per jam, bar chart per hari, heatmap
- **Tab 3 – Clustering**: Pengelompokan jam berbasis intensitas penggunaan

## 🔗 Deployment
Lihat `url.txt` untuk link dashboard yang sudah di-deploy ke Streamlit Cloud.
