import streamlit as st

st.set_page_config(
    page_title="Technical Writeup"
)

st.write(
    """
    # Wow there is text here
    """
)

with open("docs/notes/approximating-pedestrian-crash-frequency copy.md") as f:
    writeup = f.read()

st.markdown(writeup)