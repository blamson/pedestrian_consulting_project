import streamlit as st

st.set_page_config(
    page_title="Highway Safety Manual notes"
)

st.write(
    """
    # Wow there is text here
    """
)

with open("docs/notes/hsm-chapter-10-12.md") as f:
    writeup = f.read()

st.markdown(writeup)