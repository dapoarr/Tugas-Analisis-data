import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("main_data.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

# Sidebar filter
station = st.sidebar.selectbox("Pilih Stasiun", df["station"].unique())
date_min = df["datetime"].min()
date_max = df["datetime"].max()
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [date_min, date_max])
agg_option = st.sidebar.selectbox("Agregasi Waktu", ["Harian", "Mingguan", "Bulanan"])

df_filtered = df[(df["station"] == station) &
                 (df["datetime"] >= pd.to_datetime(date_range[0])) &
                 (df["datetime"] <= pd.to_datetime(date_range[1]))].copy()

# Judul
st.title("Dashboard Kualitas Udara - Beijing")
st.write(f"Data dari stasiun **{station}** dengan jumlah data: {len(df_filtered)}")

# Statistik Deskriptif Lengkap
st.subheader("Statistik Deskriptif Lengkap")
st.write(df_filtered.describe(include="all").T)

# Agregasi waktu
if agg_option == "Harian":
    df_agg = df_filtered.resample("D", on="datetime")["PM2.5"].mean()
elif agg_option == "Mingguan":
    df_agg = df_filtered.resample("W", on="datetime")["PM2.5"].mean()
else:
    df_agg = df_filtered.resample("M", on="datetime")["PM2.5"].mean()

st.subheader(f"Tren Rata-rata PM2.5 ({agg_option})")
st.line_chart(df_agg)

# Boxplot per bulan
st.subheader("Distribusi PM2.5 per Bulan")
df_filtered["month"] = df_filtered["datetime"].dt.month
fig2, ax2 = plt.subplots()
sns.boxplot(data=df_filtered, x="month", y="PM2.5", ax=ax2)
ax2.set_xlabel("Bulan")
st.pyplot(fig2)

# Korelasi heatmap semua variabel numerik
st.subheader("Heatmap Korelasi Variabel Numerik")
fig_corr, ax_corr = plt.subplots()
sns.heatmap(df_filtered.select_dtypes("number").corr(), annot=True, cmap="coolwarm", ax=ax_corr)
st.pyplot(fig_corr)

# Scatterplot interaktif antar variabel
st.subheader("Scatterplot Interaktif")
num_cols = df_filtered.select_dtypes("number").columns.tolist()
x_var = st.selectbox("Pilih variabel X", num_cols, index=0)
y_var = st.selectbox("Pilih variabel Y", num_cols, index=1)
fig_scatter, ax_scatter = plt.subplots()
sns.scatterplot(data=df_filtered, x=x_var, y=y_var, ax=ax_scatter, alpha=0.5)
st.pyplot(fig_scatter)

# Histogram PM2.5
st.subheader("Histogram PM2.5")
fig4, ax4 = plt.subplots()
sns.histplot(df_filtered["PM2.5"], bins=30, kde=True, ax=ax4)
st.pyplot(fig4)

# Tabel Data Mentah dengan pencarian
st.subheader("Data Mentah (100 baris pertama)")
search = st.text_input("Cari di data mentah:")
if search:
    st.dataframe(df_filtered[df_filtered.astype(str).apply(lambda x: search.lower() in x.str.lower().to_string(), axis=1)].head(100))
else:
    st.dataframe(df_filtered.head(100))

# Download data hasil filter
st.subheader("Download Data Hasil Filter")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, f"data_{station}.csv", "text/csv")

