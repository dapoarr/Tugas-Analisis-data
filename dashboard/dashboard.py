import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setel tema visual
st.set_page_config(
    page_title="Dashboard Kualitas Udara - Beijing",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data dari dua file di folder dataset (relative path, gunakan slash)
# Pastikan jalankan dari folder 'submission' atau sesuaikan path jika perlu
df1 = pd.read_csv("dataset/data_1.csv")
df2 = pd.read_csv("dataset/data_2.csv")
df = pd.concat([df1, df2], ignore_index=True)

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
agg_option = st.sidebar.selectbox("Agregasi Waktu", ["Harian", "Mingguan", "Bulanan"])

# Validasi input tanggal
if len(date_range) < 2:
    st.warning("Silakan pilih rentang tanggal (start date dan end date) terlebih dahulu.")
    st.stop()
else:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

df_filtered = df[
    (df["station"] == station) &
    (df["datetime"] >= start_date) &
    (df["datetime"] <= end_date)
].copy()

# Jika data tidak ada setelah filter, tampilkan pesan
if df_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

# Filter data sesuai pilihan
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])
df_filtered = df[
    (df["station"] == station) &
    (df["datetime"] >= start_date) &
    (df["datetime"] <= end_date)
].copy()

# Judul
st.title("Dashboard Kualitas Udara - Beijing")
st.write(f"Data dari stasiun **{station}** dengan jumlah data: {len(df_filtered)}")

#Fitur try-except 
#try:
#    start_date = pd.to_datetime(date_range[0])
#    end_date = pd.to_datetime(date_range[1])
#except Exception as e:
#   st.warning("Tanggal tidak valid, gunakan rentang tanggal yang benar.")
#    start_date = df["datetime"].min()
#    end_date = df["datetime"].max()


# Statistik Deskriptif
#st.subheader("Statistik Deskriptif")
#st.write(df_filtered.describe(include="all").T)

# Agregasi waktu dan visualisasi tren PM2.5
st.subheader(f"Tren Rata-rata PM2.5 ({agg_option})")
df_filtered = df_filtered.set_index("datetime")
if agg_option == "Harian":
    df_agg = df_filtered["PM2.5"].resample("D").mean()
    x_label = "Tanggal"
elif agg_option == "Mingguan":
    df_agg = df_filtered["PM2.5"].resample("W").mean()
    x_label = "Minggu"
elif agg_option == "Bulanan":
    df_agg = df_filtered["PM2.5"].resample("M").mean()
    x_label = "Bulan"

if not df_agg.empty:
    fig, ax = plt.subplots(figsize=(10, 4))
    df_agg.plot(ax=ax)
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_xlabel(x_label)
    st.pyplot(fig)
else:
    st.warning("Data tidak tersedia untuk filter yang dipilih.")

# Boxplot PM2.5 per stasiun (seperti di notebook)
st.subheader("Distribusi PM2.5 per Stasiun")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.boxplot(data=df[df["station"] == station], x="station", y="PM2.5", ax=ax2)
ax2.set_ylabel("PM2.5 (µg/m³)")
ax2.set_xlabel("Stasiun")
st.pyplot(fig2)

# Heatmap korelasi (seperti di notebook)
st.subheader("Korelasi PM2.5 dengan Faktor Cuaca")
corr_cols = ["PM2.5", "TEMP", "DEWP", "WSPM"]
corr_matrix = df_filtered[corr_cols].corr()
fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax3)
st.pyplot(fig3)

# Scatterplot PM2.5 vs WSPM dan TEMP (seperti notebook)
st.subheader("Scatterplot PM2.5 vs Kecepatan Angin dan Suhu")
fig4, (ax4, ax5) = plt.subplots(1, 2, figsize=(12, 4))
sns.scatterplot(data=df_filtered, x="WSPM", y="PM2.5", ax=ax4, alpha=0.4)
ax4.set_title("PM2.5 vs WSPM")
sns.scatterplot(data=df_filtered, x="TEMP", y="PM2.5", ax=ax5, alpha=0.4)
ax5.set_title("PM2.5 vs TEMP")
st.pyplot(fig4)

# Data mentah
#st.subheader("Data Mentah (100 baris pertama)")
#st.dataframe(df_filtered.reset_index().head(100))

# Download data hasil filter
#st.subheader("Download Data Hasil Filter")
#csv = df_filtered.reset_index().to_csv(index=False).encode('utf-8')
#st.download_button("Download CSV", csv, f"data_{station}.csv", "text/csv")