import streamlit as st

st.set_page_config(
    page_title="Granby Pedestrian Consulting Project",
    layout="wide"
)

home = st.Page("app_pages/0_Main_Page.py", title="Main Page", default=True)
background = st.Page("app_pages/1_Background.py", title="Background")
methodology = st.Page("app_pages/2_Methodology.py", title="Methodology")
data = st.Page("app_pages/3_Data_Acquisition.py", title="Data Acquisition")
results = st.Page("app_pages/4_Results_and_Interpretation.py", title="Results and Interpretation")
limitations = st.Page("app_pages/5_Limitations.py", title="Limitations")
dashboard = st.Page("app_pages/6_Dashboard.py", title="Interactive Dashboard")

pg = st.navigation({
    "": [home],
    "Methodology and Results": [background, methodology, data, results, limitations],
    "Tools": [dashboard],
})

pg.run()