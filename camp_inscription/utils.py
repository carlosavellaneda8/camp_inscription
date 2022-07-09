import streamlit as st


def read_local_css(file_name):
    """Reads a local CSS file to format markdown"""
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
