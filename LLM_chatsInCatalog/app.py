import streamlit as st
from main import main as run_main

st.set_page_config(layout="wide", page_title="Chats in Use Case Catalog", page_icon="vectorlogo600.png")

def display_existing_messages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_user_message_to_session(prompt):
    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

def add_message_to_session(role, content):
    st.session_state["messages"].append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)

def print_markdown_from_file(file_path):
    with open(file_path, "r") as f:
        markdown_content = f.read()
        st.markdown(markdown_content, unsafe_allow_html=True)

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

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='color: #ec008c;'>The Vector Institute USE CASE CHAT GENERATOR</h1>", unsafe_allow_html=True)
    st.write("**A Knowledge Based Retrieval of relevant Vector Projects' Use Cases**")
    st.sidebar.image("vectorlogo600.png", width=130)

    hide_streamlit_header_footer()
    display_existing_messages()

    query_text = st.chat_input("Enter your question:")
    response = None

    if query_text:
        add_message_to_session("user", query_text)
        with st.spinner("Retrieving Response..."):
            response = run_main(query_text)
            add_message_to_session("assistant", response)

    with st.sidebar:
        print_markdown_from_file("utilities/members.md")

    return response

if __name__ == "__main__":
    response = main()
