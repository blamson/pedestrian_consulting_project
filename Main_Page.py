import streamlit as st

st.set_page_config(
    page_title="Granby Pedestrian Consulting Project",
    layout="wide"
)

home = st.Page("pages/1_writeup.py", title="Main Page", default=True)
# background = st.Page("app_pages/1_Background.py", title="Background")
# methodology = st.Page("app_pages/2_Methodology.py", title="Methodology")
# data = st.Page("app_pages/3_Data_Acquisition.py", title="Data Acquisition")
# results = st.Page("app_pages/4_Results_and_Interpretation.py", title="Results and Interpretation")
# limitations = st.Page("app_pages/5_Limitations.py", title="Limitations")
accident_rates_dashboard = st.Page("pages/6_Accident_Rates.py", title="Accident Rates")
long_term_risk_dashboard = st.Page("pages/7_Long_Term_Risk.py", title="Long Term Risk")
tinkering = st.Page("pages/8_tinkering.py", title="Messin about")
tinkering2 = st.Page("pages/9_tinkering2.py", title="Messin about2")

pg = st.navigation({
    "": [home],
    # "Methodology and Results": [background, methodology, data, results, limitations],
    "Tools": [accident_rates_dashboard, long_term_risk_dashboard, tinkering, tinkering2],
})

pg.run()