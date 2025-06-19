import streamlit as st
import folium
from streamlit_folium import st_folium


def app():
    st.title("Spatial Distribution of Mangrove Density in Tanjung Pinang and Bintan")
    st.write("This map displays the density of mangrove vegetation in Bintan and "
             "Tanjung Pinang, derived from the classification of 2013 Landsat imagery.")

    try:
        import geopandas as gpd
        gdf = gpd.read_file("data/BintanTjPngMangrove.shp")
        gdf = gdf.to_crs(epsg=4326)

        m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()],
                       zoom_start=12)

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
            tooltip=folium.GeoJsonTooltip(
                fields=["KRTJ", "SHAPE_Area"],
                aliases=["Density: ", "Area (ha): "]
            )
        ).add_to(m)

        st_folium(m, width=700, height=500)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat shapefile: {e}")
