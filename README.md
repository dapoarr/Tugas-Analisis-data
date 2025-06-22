<<<<<<< HEAD
# Dashboard Kualitas Udara - Beijing

Proyek ini merupakan dashboard interaktif untuk analisis kualitas udara di Beijing menggunakan data PM2.5 dan variabel cuaca lainnya. Dashboard dibangun dengan Python, pandas, seaborn, matplotlib, dan Streamlit.

## Fitur

- **Dasar-Dasar Analisis Data:**  
  Menampilkan struktur data, tipe data, dan pemeriksaan missing values.

- **Statistik Deskriptif:**  
  Statistik ringkasan (mean, median, min, max, dst) untuk seluruh variabel.

- **Data Wrangling:**  
  Pembersihan data, penanganan missing values, dan filtering data.

- **Exploratory Data Analysis (EDA):**  
  Analisis distribusi, tren, dan korelasi antar variabel.

- **Visualisasi Data:**  
  Line chart, boxplot, histogram, scatterplot, dan heatmap korelasi.

- **Dashboard Interaktif:**  
  Filter berdasarkan stasiun dan rentang tanggal, serta download data hasil filter.

## Cara Menjalankan

1. **Clone repository:**
   ```
   git clone hhttps://github.com/dapoarr/Tugas-Analisis-data
   cd Dashboard-Kualitas-Udara---Beijing-
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Jalankan dashboard:**
   ```
   streamlit run main_analysis_dashboard.py
   ```

4. **Akses dashboard di browser** pada alamat yang tertera di terminal.

## Struktur Data

Pastikan file `main_data.csv` berada di folder `dashboard/` dengan kolom minimal:
- `datetime`
- `station`
- `PM2.5`
- `TEMP`
- `DEWP`
- `WSPM`
- (dan variabel lain jika ada)

## Lisensi

Proyek ini bebas digunakan untuk keperluan pembelajaran dan non-komersial.

---

**Dikembangkan oleh:**
M Dafa Ar Rasyid
=======
# Tugas-Analisis-data
Project Data Analisys kualitas udara, untuk memenuhi materi Coding camp
>>>>>>> 646496085b98a00ac150b8b8ff2d1caee6425bde
