import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Edited to add earthquake map
# Navigasi sidebar
menu = st.sidebar.selectbox(
    "Pilih Halaman", ["Home", "Jabodetabek Earthquake Map", "About"])

# Konten halaman
if menu == "Home":
    st.title("Welcome to My Mini Project")
    st.write("Ini adalah halaman utama aplikasi Streamlit Asri-f.")

# Halaman Peta Gempa
elif menu == "Peta Gempa":
    st.title("Peta Sebaran Gempa")
    st.write("Visualisasi lokasi gempa berdasarkan data dari USGS.")

    # Load data CSV
    df = pd.read_csv("eq_singkat.csv")

    # Cek isi data
    st.write("Contoh data:", df.head())

    # Inisialisasi peta (posisi awal di sekitar Jakarta)
    m = folium.Map(location=[-6.2, 106.8], zoom_start=6)

    # Tambahkan marker untuk tiap gempa
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['mag'] * 2,  # Magnitudo sebagai ukuran
            color='red' if row['mag'] >= 5 else 'orange',
            fill=True,
            fill_opacity=0.6,
            popup=folium.Popup(
                f"Mag: {row['mag']}<br>Depth: {row['depth']} km<br>{row['place']}", max_width=300)
        ).add_to(m)

    # Tampilkan di Streamlit
    st_folium(m, width=700, height=500)


elif menu == "About":
    st.title("Tentang Aplikasi")
    st.write("Aplikasi ini dibuat untuk menampilkan peta interaktif dan info lainnya.")
