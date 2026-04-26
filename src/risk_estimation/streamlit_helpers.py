import streamlit as st
import polars as pl

@st.cache_data
def load_data(path):
    df = pl.read_csv(path)
    return df