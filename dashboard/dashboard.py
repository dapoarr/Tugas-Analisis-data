import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Setel tema visual
st.set_page_config(
    page_title="Dashboard Kualitas Udara - Beijing",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data main_data.csv yang sudah bersih
data_path = "dashboard/main_data.csv"
if not os.path.exists(data_path):
    data_path = "main_data.csv"  # fallback jika dijalankan dari folder dashboard

try:
    df = pd.read_csv(data_path)
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

# Pastikan kolom datetime ada dan bertipe datetime
if 'datetime' not in df.columns:
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
else:
    df["datetime"] = pd.to_datetime(df["datetime"])

# Sidebar filter
st.sidebar.title("Filter Data")
station = st.sidebar.selectbox("Pilih Stasiun", df["station"].unique())
date_min = df["datetime"].min().date()
date_max = df["datetime"].max().date()
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [date_min, date_max])

# Validasi input tanggal
if len(date_range) < 2:
    st.warning("Silakan pilih rentang tanggal (start date dan end date) terlebih dahulu.")
    st.stop()
else:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

# Filter data sesuai pilihan
df_filtered = df[
    (df["station"] == station) &
    (df["datetime"] >= start_date) &
    (df["datetime"] <= end_date)
].copy()

# Judul dan info data
st.title("Dashboard Kualitas Udara - Beijing")
st.markdown(f"""
**Pertanyaan Bisnis:**
1. Bagaimana perbandingan tren bulanan rata-rata PM2.5 antara dua stasiun: Aotizhongxin dan Changping?
2. Apa pengaruh faktor cuaca (suhu, kelembapan, dan kecepatan angin) terhadap kadar PM2.5 di kedua stasiun?
""")
st.write(f"Data dari stasiun **{station}** dengan jumlah data: {len(df_filtered)}")
st.dataframe(df_filtered.head())

# 1. Distribusi PM2.5 per stasiun (Boxplot)
st.subheader("Distribusi PM2.5 per Stasiun")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.boxplot(data=df[df["station"] == station], x="station", y="PM2.5", ax=ax1)
ax1.set_ylabel("PM2.5 (µg/m³)")
ax1.set_xlabel("Stasiun")
st.pyplot(fig1)
st.markdown(
    """
    **Insight:**  
    - Stasiun Aotizhongxin cenderung memiliki median PM2.5 lebih tinggi dibanding Changping.
    - Sebaran PM2.5 di Aotizhongxin juga lebih bervariasi.
    """
)

# 2. Korelasi PM2.5 dengan Faktor Cuaca (Heatmap)
st.subheader("Korelasi PM2.5 dengan Faktor Cuaca")
corr_cols = ["PM2.5", "TEMP", "DEWP", "WSPM"]
corr_matrix = df_filtered[corr_cols].corr()
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax2)
st.pyplot(fig2)
st.markdown(
    """
    **Insight:**  
    - PM2.5 berkorelasi negatif dengan WSPM (kecepatan angin), artinya polusi menurun saat angin lebih kencang.
    - Korelasi dengan suhu (TEMP) dan kelembapan (DEWP) sangat lemah.
    """
)

# 3. Tren Bulanan Rata-rata PM2.5 per Stasiun (Lineplot)
st.subheader("Tren Bulanan Rata-rata PM2.5 per Stasiun")
df['month_str'] = df['datetime'].dt.to_period('M').astype(str)
monthly_pm = df.groupby(['month_str', 'station'])['PM2.5'].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(14, 6))
sns.lineplot(data=monthly_pm, x='month_str', y='PM2.5', hue='station', ax=ax3)
ax3.set_title('Tren Bulanan Rata-rata PM2.5 per Stasiun')
ax3.set_ylabel('Rata-rata PM2.5 (µg/m³)')
ax3.set_xlabel('Bulan')
plt.xticks(rotation=45)
ax3.legend(title='Stasiun')
st.pyplot(fig3)
st.markdown(
    """
    **Insight:**  
    - Aotizhongxin memiliki puncak PM2.5 yang lebih tinggi dan lebih sering dari Changping.
    - Kedua stasiun menunjukkan tren menurun pada pertengahan tahun (musim panas).
    """
)

# 4. Scatterplot PM2.5 vs Kecepatan Angin dan Suhu (per stasiun)
st.subheader("Scatterplot PM2.5 vs Kecepatan Angin dan Suhu")
fig4, (ax4, ax5) = plt.subplots(1, 2, figsize=(12, 4))
sns.scatterplot(data=df_filtered, x="WSPM", y="PM2.5", hue="station", ax=ax4, alpha=0.4)
ax4.set_title("PM2.5 vs Kecepatan Angin")
sns.scatterplot(data=df_filtered, x="TEMP", y="PM2.5", hue="station", ax=ax5, alpha=0.4)
ax5.set_title("PM2.5 vs Suhu")
st.pyplot(fig4)
st.markdown(
    """
    **Insight:**  
    - PM2.5 cenderung menurun saat kecepatan angin meningkat di kedua stasiun.
    - Tidak ada hubungan kuat antara suhu dan PM2.5.
    """
)