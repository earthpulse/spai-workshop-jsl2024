"""
Streamlit app with Folium to display analytics
"""

import os

import folium
from streamlit_folium import folium_static
import geopandas as gpd
import pandas as pd
import requests
import streamlit as st

from spai.config import SPAIVars

vars = SPAIVars()


def get_aoi_centroid():
    """
    Get AoI centroid

    Returns
    -------
    centroid : tuple
        AOI centroid
    """
    aoi = vars["AOI"]
    gdf = gpd.GeoDataFrame.from_features(aoi)
    centroid = gdf.geometry.centroid[0].y, gdf.geometry.centroid[0].x

    return centroid


@st.cache_data(ttl=10)
def get_data():
    api_url = "http://" + os.getenv("ANALYTICS_URL")
    analytics = requests.get(api_url).json()
    analytics_df = pd.DataFrame(analytics)
    analytics_df.sort_index(inplace=True)

    return analytics_df


def choose_variables():
    """
    Choose date and variable from the analytics data

    Returns
    -------
    date : str
        Date from the analytics data
    variable : str
        Variable from the analytics data
    """
    base_df = get_data()
    with st.sidebar:
        st.sidebar.markdown("### Select date ")
        date = st.selectbox("Date", base_df.index)

    return date


st.set_page_config(page_title="SPAI demo", page_icon="🌏")

date = choose_variables()  # Choose date and variable from the data
dataframe = get_data()
centroid = get_aoi_centroid()  # Get centroid from the AOI

url = f"http://{os.getenv('XYZ_URL')}/NDVI_{date}.tif/{{z}}/{{x}}/{{y}}.png"

m = folium.Map(
    location=centroid,
    zoom_start=12,
    tiles="CartoDB Positron",
)
# Add the analytic layer to the map
raster = folium.raster_layers.TileLayer(
    tiles=url,
    attr="Forest monitoring Pulse",
    name="Vegetation",
    overlay=True,
    control=True,
    show=True,
)
raster.add_to(m)
folium_static(m)

# Plot vegetation analytics data
st.title("Vegetation Analytics")

colors = ["#e41a1c", "#BFEAA2", "#E4EA20", "#245900"]

# Remove Total column to not plot it
df_chart = (
    dataframe.drop(columns=["Total"]) if "Total" in dataframe.columns else dataframe
)
st.line_chart(df_chart)
if st.checkbox("Show data"):
    st.write(dataframe)
