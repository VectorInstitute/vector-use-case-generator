import streamlit as st
from data_loader import load_use_cases, filter_use_cases
from ui_components import display_use_case_card, display_use_cases, generate_card_image
from app_config import set_page_config, hide_streamlit_header_footer
from utils import handle_null


def main():
    set_page_config()
    hide_streamlit_header_footer()
    st.title("The Vector Institute Use Case Catalog")

    # Load data
    use_cases_df = load_use_cases("data/Updated Vector Use Case Catalog.xlsx")

    # Initialize session state
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    if 'search_input' not in st.session_state:
        st.session_state.search_input = ""

    # Sidebar controls
    st.sidebar.image("data/vectorlogo600.png", width=130)

    st.sidebar.markdown("<h3>Filters</h3>", unsafe_allow_html=True)
    show_all = st.sidebar.checkbox("Show All Use Cases")

    # Search functionality
    search_query = st.text_input("Search for a use case:", key="search_input")
    if st.session_state.search_input != search_query:
        st.session_state.search_input = search_query

    # Filter use cases
    filtered_use_cases = filter_use_cases(use_cases_df, search_query, show_all)

    # Display use cases
    display_use_cases(filtered_use_cases, show_all)

if __name__ == "__main__":
    main()