import streamlit as st

# Navigasi sidebar
menu = st.sidebar.selectbox("Pilih Halaman", ["Home", "About"])

# Konten halaman
if menu == "Home":
    st.title("Selamat Datang di Aplikasi Saya")
    st.write("Ini adalah halaman utama aplikasi Streamlit Asri-f.")

elif menu == "About":
    st.title("Tentang Aplikasi")
    st.write("Aplikasi ini dibuat untuk menampilkan peta interaktif dan info lainnya.")
