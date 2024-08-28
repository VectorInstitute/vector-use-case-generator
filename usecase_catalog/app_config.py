import streamlit as st

def set_page_config():
    st.set_page_config(layout="wide", page_title="Use Case Catalog", page_icon="vectorlogo600.png")

    st.markdown("""
    <style>
    .use-case-card {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .use-case-table {
        width: 100%;
        border-collapse: collapse;
    }
    .use-case-table th, .use-case-table td {
        border: 1px solid #ec008c;
        padding: 8px;
    }
    .use-case-table th {
        background-color: #ec008c;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def hide_streamlit_header_footer():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
        </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def set_custom_css():
    st.markdown("""
    <style>
    .use-case-card {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .use-case-table {
        width: 100%;
        border-collapse: collapse;
    }
    .use-case-table th, .use-case-table td {
        border: 1px solid #ec008c;
        padding: 8px;
    }
    .use-case-table th {
        background-color: #ec008c;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)