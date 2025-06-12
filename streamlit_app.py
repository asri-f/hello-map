import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Edited to add earthquake map
# Navigasi sidebar
menu = st.sidebar.selectbox(
    "Pilih Halaman", ["Home", "Earthquake Map", "About"])

# Konten halaman
if menu == "Home":
    st.title("Welcome to My Mini Project")
    st.write("This is the main page of the Streamlit app created by Asri-f.")
    st.markdown(
        "Use the sidebar to navigate between the earthquake map and app information."
    )

# Halaman Peta Gempa
elif menu == "Earthquake Map":
    st.title("Earthquake Distribution Map")
    st.write("Visualization of earthquake locations based on USGS data from the past 10 years "
             "in the DKI Jakarta area, West Java, and surrounding regions, "
             "with magnitudes greater than 5.")

    try:
        df = pd.read_csv("eq_singkat.csv")
        st.markdown("**Example Data:**")
        st.dataframe(df.head())

        # Initialize the map
        m = folium.Map(location=[-6.2, 106.8], zoom_start=8)

        # Add markers
        for _, row in df.iterrows():
            # Tentukan warna berdasarkan magnitudo
            mag = row['mag']
            if 5.0 <= mag < 5.5:
                color = 'yellow'
            elif 5.5 <= mag < 6.0:
                color = 'orange'
            else:  # mag >= 6.0
                color = 'red'

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=mag * 2,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(
                    f"<b>Magnitude:</b> {mag}<br><b>Depth:</b> {row['depth']} km<br><b>Location:</b> {row['place']}<br><b>Time:</b> {row['time']}",
                    max_width=300),
                tooltip=f"{row['place']} (M {mag})"
            ).add_to(m)

        # Display map
        st_folium(m, width=700, height=500)

    except FileNotFoundError:
        st.error(
            "Data file 'eq_singkat.csv' not found. Please make sure it's in the correct directory.")

# About page
elif menu == "About":
    st.title("About This App")
    st.write(
        "This mini project app was created to display an interactive map related to environmental and disaster topics. "
        "It visualizes earthquake data sourced from USGS focused on the Jakarta region and surroundings."
    )
    st.markdown(
        "**Feel free to share or contact me if you're interested!**\n\n"
        "Created by Asri-f."
    )
