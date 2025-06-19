import streamlit as st
from pages import home, earthquake, mangrove, about

# Sidebar untuk navigasi
menu = st.sidebar.selectbox(
    "Index",
    ["Home", "Earthquake Map", "Mangrove Density Map", "About"]
)

# Routing ke halaman sesuai pilihan
if menu == "Home":
    home.app()
elif menu == "Earthquake Map":
    earthquake.app()
elif menu == "Mangrove Density Map":
    mangrove.app()
elif menu == "About":
    about.app()
