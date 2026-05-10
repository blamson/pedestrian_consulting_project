import streamlit as st

st.set_page_config(
    page_title="Granby Pedestrian Consulting Project",
    layout="wide"
)

# Home
home = st.Page("app_pages/0_Main_Page.py", title="Main Page", default=True)

# Report sections
background = st.Page("app_pages/1_Background.py", title="Background")
methods_hsm = st.Page("app_pages/2_Methods_HSM_Intro.py", title="Methods: HSM Intro")
methods_spfs = st.Page("app_pages/3_Methods_SPFs.py", title="Methods: SPFs")
methods_cmfs = st.Page("app_pages/4_Methods_CMFs.py", title="Methods: CMFs")
data = st.Page("app_pages/5_Data_Acquisition.py", title="Data Acquisition")
results = st.Page("app_pages/6_Results_and_Interpretation.py", title="Results and Interpretation")
limitations = st.Page("app_pages/7_Limitations.py", title="Limitations")

# Interactive tools (his new pages)
accident_rates = st.Page("app_pages/8_Accident_Rates.py", title="📊 Accident Rates")
long_term_risk = st.Page("app_pages/9_Long_Term_Risk.py", title="📊 Long Term Risk")
simulation = st.Page("app_pages/10_Simulation.py", title="🎲 Simulation")
bulk_simulation = st.Page("app_pages/11_Bulk_Simulation.py", title="🎲 Bulk Simulation")

pg = st.navigation({
    "": [home],
    "Methodology and Results": [background, methods_hsm, methods_spfs, methods_cmfs, data, results, limitations],
    "Interactive Tools": [accident_rates, long_term_risk, simulation, bulk_simulation],
})
pg.run()