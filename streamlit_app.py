import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Edited to add earthquake map
# Navigasi sidebar
menu = st.sidebar.selectbox(
    "Pilih Halaman", ["Home", "Earthquake Map", "Mangrove Density Map", "About"])

# Konten halaman
if menu == "Home":
    st.title("Welcome to My Mini Project")
    st.write("This page of the Streamlit app created by Asri F.")
    st.markdown(
        "Use the sidebar to navigate app information."
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

# Mangrove Density Map
elif menu == "Mangrove Density Map":
    st.title("Spatial Distribution of Mangrove Density in Tanjung Pinang and Bintan")
    st.write("This map displays the density of mangrove vegetation in Bintan and "
             "Tanjung Pinang, derived from the classification of 2013 Landsat imagery.")

    try:
        import geopandas as gpd

        # Load shapefile mangrove
        # sesuaikan path jika beda
        gdf = gpd.read_file("data/BintanTjPngMangrove.shp")
        gdf = gdf.to_crs(epsg=4326)  # pastikan pakai lat/lon

        # Peta dasar
        m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()],
                       zoom_start=11)

        # Warna berdasarkan klasifikasi KRTJ
        color_dict = {
            'mangrove lebat': 'green',
            'mangrove sedang': 'yellow',
            'mangrove jarang': 'red'
        }

        def style_function(feature):
            klasifikasi = feature['properties']['KRTJ'].lower()
            return {
                'fillColor': color_dict.get(klasifikasi, 'gray'),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.6
            }

        folium.GeoJson(
            gdf,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(fields=["KRTJ", "SHAPE_Area"], aliases=[
                                          "Density: ", "Area (ha): "])
        ).add_to(m)

        # Tampilkan di Streamlit
        st_folium(m, width=700, height=500)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat shapefile: {e}")


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
