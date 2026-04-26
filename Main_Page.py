import streamlit as st
import polars as pl

st.title("Hello world")

# st.markdown('## Results Table')
results_table = pl.read_csv("data/results/results_2026-04-19.csv")
# st.dataframe(table, width='stretch')

# st.markdown('## SPF Table')
spf_table = pl.read_csv("data/spfs.csv")
# st.dataframe(spf_table, width='stretch')

st.markdown('## OOOO interactive')
intersection = st.selectbox(
    label="Please select an intersection",
    options=("Agate & Mesa", "Agate & 4th"),
    index=0,
)

intersection_results = (
    results_table
    .filter(pl.col("intersection_name") == intersection)
)

st.dataframe(intersection_results)