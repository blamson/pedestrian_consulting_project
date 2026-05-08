import streamlit as st

st.set_page_config(
    page_title="Granby Pedestrian Consulting Project",
    layout="wide"
)

# Home
home = st.Page("app_pages/0_Main_Page.py", title="Main Page", default=True)

# Report sections
background = st.Page("app_pages/1_Background.py", title="Background")
methodology = st.Page("app_pages/2_Methodology.py", title="Methodology")
data = st.Page("app_pages/3_Data_Acquisition.py", title="Data Acquisition")
results = st.Page("app_pages/4_Results_and_Interpretation.py", title="Results and Interpretation")
limitations = st.Page("app_pages/5_Limitations.py", title="Limitations")

# Interactive tools (his new pages)
accident_rates = st.Page("app_pages/6_Accident_Rates.py", title="📊 Accident Rates")
long_term_risk = st.Page("app_pages/7_Long_Term_Risk.py", title="📊 Long Term Risk")
simulation = st.Page("app_pages/8_Simulation.py", title="🎲 Simulation")
bulk_simulation = st.Page("app_pages/9_Bulk_Simulation.py", title="🎲 Bulk Simulation")

pg = st.navigation({
    "": [home],
    "Methodology and Results": [background, methodology, data, results, limitations],
    "Interactive Tools": [accident_rates, long_term_risk, simulation, bulk_simulation],
})

pg.run()