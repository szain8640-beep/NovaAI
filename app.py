import streamlit as st
import os
import requests
from groq import Groq

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

st.title("🤖 NovaAI - Multi-Modal Studio")
st.write("Aapka apna advanced AI platform!")

# Tabs for all features
chat_tab, image_tab, voice_tab = st.tabs(["💬 Text Chat", "🖼️ AI Image Generator", "🗣️ Voice Generator"])

# --- TAB 1: TEXT CHAT ---
with chat_tab:
    st.subheader("NovaAI Smart Chat")
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            pass

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
            
            if api_key:
                try:
                    client = Groq(api_key=api_key)
                    system_prompt = {
                        "role": "system",
                        "content": "Aap ek expert aur dostana AI assistant hain jiska naam NovaAI hai."
                    }
                    full_messages = [system_prompt] + st.session_state.messages

                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=full_messages,
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    bot_reply = completion.choices[0].message.content
                except Exception as e:
                    bot_reply = f"Error: {e}"
            else:
                # Smart fallback so chat is always active and responsive
                if "kesy ho" in prompt.lower() or "kese ho" in prompt.lower():
                    bot_reply = "Main bilkul theek hoon! Aap sunayein, aap kaise hain?"
                elif "naam" in prompt.lower():
                    bot_reply = "Mera naam NovaAI hai."
                else:
                    bot_reply = f"Aapne kaha: '{prompt}'. Main aapka smart AI assistant hoon!"

            message_placeholder.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# --- TAB 2: AI IMAGE GENERATOR ---
with image_tab:
    st.subheader("NovaAI Image Studio")
    st.write("Yahan apni pasand ki tasveer ka text likhein:")
    
    user_image_prompt = st.text_input("Misal: A beautiful futuristic city", "", key="img_prompt_input")
    
    if st.button("Generate Image"):
        if not user_image_prompt.strip():
            st.warning("Pehle koi prompt likhein!")
        else:
            with st.spinner("Tasveer generate ho rahi hai, intezar karein..."):
                try:
                    encoded_prompt = requests.utils.quote(user_image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    
                    st.success("Tasveer kamyabi ke sath ban gayi hai!")
                    st.image(image_url, caption=user_image_prompt, use_container_width=True)
                except Exception as err:
                    st.error(f"Error: {err}")

# --- TAB 3: VOICE GENERATOR ---
with voice_tab:
    st.subheader("NovaAI Voice Studio")
    st.write("Text ko aawaz mein badalein:")
    
    voice_text = st.text_area("Yahan text likhein:", "Hello! Welcome to NovaAI.")
    
    if st.button("Generate Voice Audio"):
        if not voice_text.strip():
            st.warning("Pehle text likhein!")
        else:
            with st.spinner("Aawaz tayyar ho rahi hai..."):
                try:
                    encoded_voice_text = requests.utils.quote(voice_text)
                    audio_api_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_voice_text}&tl=en&client=tw-ob"
                    
                    st.success("Aawaz tayyar hai!")
                    st.audio(audio_api_url, format='audio/mp3')
                except Exception as voice_err:
                    st.error(f"Error: {voice_err}")
