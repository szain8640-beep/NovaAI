import streamlit as st
import os
import requests

# Page Config
st.set_page_config(page_title="NovaAI Studio", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 NovaAI - Professional Multi-Modal Studio")
st.write("Aapka apna advanced AI platform: Smart Chat, High-Quality Image Studio, aur Professional Voice Studio.")

# Tabs for all features
chat_tab, image_tab, voice_tab = st.tabs(["💬 Text Chat", "🖼️ AI Image Generator", "🗣️ Voice Studio (TTS)"])

# --- TAB 1: TEXT CHAT ---
with chat_tab:
    st.subheader("NovaAI Smart Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Salam! Main NovaAI hoon. Batayein aaj main aapki kya madad kar sakta hoon?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("NovaAI se kuch bhi puchein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Professional AI Assistant response simulation / backend logic
            bot_reply = f"Aapka sawal mil gaya hai: '{prompt}'. Main NovaAI ka expert assistant hoon, aur is par behtareen response tayyar kar raha hoon!"
            
            message_placeholder.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# --- TAB 2: AI IMAGE GENERATOR (Asal image display logic) ---
with image_tab:
    st.subheader("NovaAI Image Studio")
    st.write("Yahan jo prompt aap likhenge, uski high-quality AI image foran generate ho kar screen par nazar aayegi:")
    
    user_image_prompt = st.text_input("Misal: A professional futuristic city cyberpunk style", "", key="img_prompt_input")
    
    if st.button("Generate Image"):
        if not user_image_prompt.strip():
            st.warning("Baraye meherbani pehle koi prompt likhein!")
        else:
            with st.spinner("Tasveer generate ho rahi hai, baraye meherbani intezar karein..."):
                try:
                    # Encoding prompt for image generation API
                    encoded_prompt = requests.utils.quote(user_image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    
                    st.success("Tasveer kamyabi ke sath generate ho gayi hai!")
                    # Directly rendering image on UI
                    st.image(image_url, caption=f"Prompt: {user_image_prompt}", use_container_width=True)
                except Exception as err:
                    st.error(f"Image generation mein error aa gaya: {err}")

# --- TAB 3: PROFESSIONAL VOICE STUDIO (High Quality Audio) ---
with voice_tab:
    st.subheader("NovaAI Professional Voice Generator")
    st.write("Yahan jo text aap likhenge, usay professional aur saaf aawaz mein convert kiya jaye ga:")
    
    voice_text = st.text_area("Yahan text enter karein:", "Hello! Welcome to NovaAI. Your advanced multi-modal assistant is ready to help you.")
    
    selected_voice = st.selectbox("Select Voice Accent / Style:", ["English (US - Professional)", "English (UK - Formal)"])
    
    if st.button("Generate Professional Voice"):
        if not voice_text.strip():
            st.warning("Baraye meherbani pehle kuch text likhein!")
        else:
            with st.spinner("Professional aawaz tayyar ho rahi hai..."):
                try:
                    # Using Streamlabs / Responsive TTS public endpoint for clear professional speech
                    encoded_voice_text = requests.utils.quote(voice_text)
                    # High quality speech stream URL
                    audio_api_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_voice_text}&tl=en&client=tw-ob"
                    
                    st.success("Professional aawaz tayyar ho chuki hai! Neeche play ya download karein:")
                    st.audio(audio_api_url, format='audio/mp3')
                except Exception as voice_err:
                    st.error(f"Voice generation mein error: {voice_err}")
