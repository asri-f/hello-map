import streamlit as st
import pandas as pd
import folium
import os
from streamlit_folium import st_folium


def app():
    st.title("Earthquake Distribution Map")
    st.write("Visualization of earthquake locations based on USGS data from the past 10 years "
             "in the DKI Jakarta area, West Java, and surrounding regions, "
             "with magnitudes greater than 5.")

    try:
        st.write("📁 Files in current directory:", os.listdir("."))
        # baris debug penting
        st.write("📁 Files in data/:", os.listdir("data"))

        df = pd.read_csv("data/eq_singkat.csv")  # Pastikan path benar
        st.markdown("**Example Data:**")
        st.dataframe(df.head())

        # Tambahkan tombol download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data CSV",
            data=csv,
            file_name='earthquake_data.csv',
            mime='text/csv'
        )

        # Peta
        m = folium.Map(location=[-6.2, 106.8], zoom_start=8)

        for _, row in df.iterrows():
            mag = row['mag']
            color = 'yellow' if 5.0 <= mag < 5.5 else 'orange' if 5.5 <= mag < 6.0 else 'red'

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=mag * 2,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(
                    f"<b>Magnitude:</b> {mag}<br><b>Depth:</b> {row['depth']} km<br>"
                    f"<b>Location:</b> {row['place']}<br><b>Time:</b> {row['time']}",
                    max_width=300),
                tooltip=f"{row['place']} (M {mag})"
            ).add_to(m)

        st_folium(m, width=700, height=500)

    except FileNotFoundError:
        st.error(
            "Data file 'data/eq_singkat.csv' not found. Please make sure it's in the correct directory.")
