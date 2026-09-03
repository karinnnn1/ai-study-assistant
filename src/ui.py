import streamlit as st


def show_home(title: str, description: str) -> None:
    """Display the home page."""
    st.title(title)
    st.write(description)