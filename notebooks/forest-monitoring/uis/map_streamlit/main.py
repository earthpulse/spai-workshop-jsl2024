"""
Streamlit app with Folium to display vegetation analytics
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

ANALYTICS_URL = f'http://{os.getenv("ANALYTICS_URL")}'
XYZ_URL = f'http://{os.getenv("XYZ_URL")}'


VARIABLES_STRETCH = {
    "Vegetation": "0,1",
    "Quality": "0,3",
}

ANALYTICS_TABLES = {
    "Vegetation": "AOI_Vegetation_Growth",
    "Quality": "AOI_Vegetation_Quality",
}

VARIABLES_COLORS = {
    "Vegetation": ["#e41a1c", "#245900"],
    "Quality": ["#e41a1c", "#BFEAA2", "#E4EA20", "#245900"],
}


@st.cache_data(ttl=10)
def get_data(analytics_file: str):
    """
    Get vegetation analytics data

    Parameters
    ----------
    analytics_file : str
        Name of analytics file

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with vegetation analytics data
    """
    api_url = ANALYTICS_URL
    analytics = requests.get(f"{api_url}/{analytics_file}", timeout=10).json()
    analytics_df = pd.DataFrame(analytics)
    analytics_df.sort_index(inplace=True)

    return analytics_df


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
    base_df = get_data("AOI_Vegetation_Growth")
    with st.sidebar:
        st.sidebar.markdown("### Select date and indicator")
        date = st.selectbox("Date", base_df.index)
        variable = st.selectbox("Indicator", ["Vegetation", "Quality"])
        analytics_file = ANALYTICS_TABLES[variable]
        df = get_data(analytics_file)

    return date, variable, df


st.set_page_config(page_title="Forest monitoring Pulse", page_icon="🌳")

centroid = get_aoi_centroid()  # Get centroid from the AOI

date, variable, dataframe = choose_variables()  # Choose date and variable from the data

url = f"{XYZ_URL}/{variable.lower()}_masked_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=RdYlGn&stretch={VARIABLES_STRETCH[variable]}"

# Create map with Folium
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
st.line_chart(df_chart, color=VARIABLES_COLORS[variable])
if st.checkbox("Show data"):
    st.write(dataframe)
