import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="NovaAI Studio",
    page_icon="🤖",
    layout="centered"
)

# Main Title
st.title("🤖 NovaAI - Fresh Start")
st.write("Aapka apna naya aur mukammal AI platform zero se build ho raha hai!")

# Simple test text input to check responsiveness
user_input = st.text_input("Yahan apna naam ya koi message likhein:")
if user_input:
    st.success(s.format(user_input) if 's' else f"Welcome, {user_input}! NovaAI ka naya foundation tayyar hai.")
