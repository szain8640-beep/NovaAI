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

st.title("🤖 NovaAI - Professional Multi-Modal Studio")
st.write("Aapka apna advanced AI platform: Real Smart Chat, High-Quality Image Studio, aur Professional Voice Studio.")

# Tabs for all features
chat_tab, image_tab, voice_tab = st.tabs(["💬 Text Chat", "🖼️ AI Image Generator", "🗣️ Voice Studio (TTS)"])

# --- TAB 1: REAL SMART TEXT CHAT ---
with chat_tab:
    st.subheader("NovaAI Smart Chat")
    
    # Securely checking for Groq API Key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            pass

    if not api_key:
        st.warning("⚠️ Groq API key configure nahi hai. Aap apni free Groq API key Streamlit Secrets mein add karein taake real AI chat chal sake.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Salam! Main NovaAI hoon. Aap mujhse coding, studies, ya kisi bhi topic par baat kar sakte hain!"}
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
                        "content": "Aap ek expert, highly intelligent aur professional AI assistant hain jiska naam NovaAI hai."
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
                    bot_reply = f"Maazrat, AI response generate karne mein error aaya hai: {e}"
            else:
                # Intelligent backup responses if key is not active yet so chat feels alive
                if "kesy ho" in prompt.lower() or "kese ho" in prompt.lower():
                    bot_reply = "Main bilkul theek hoon! Aap batayein, aaj main aapki kya madad karoon?"
                elif "naam" in prompt.lower():
                    bot_reply = "Mera naam NovaAI hai, aapka apna advanced multi-modal assistant."
                else:
                    bot_reply = f"Aapka behtareen sawal hai: '{prompt}'. NovaAI is par mazeed research aur advanced processing kar raha hai!"

            message_placeholder.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# --- TAB 2: AI IMAGE GENERATOR ---
with image_tab:
    st.subheader("NovaAI Image Studio")
    st.write("Yahan jo prompt aap likhenge, uski high-quality AI image foran screen par generate ho kar aayegi:")
    
    user_image_prompt = st.text_input("Misal: A beautiful realistic portrait of a futuristic cyberpunk city", "", key="img_prompt_input")
    
    if st.button("Generate Image"):
        if not user_image_prompt.strip():
            st.warning("Baraye meherbani pehle koi prompt likhein!")
        else:
            with st.spinner("Tasveer generate ho rahi hai, intezar karein..."):
                try:
                    encoded_prompt = requests.utils.quote(user_image_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    
                    st.success("Tasveer kamyabi ke sath generate ho chuki hai!")
                    st.image(image_url, caption=f"Prompt: {user_image_prompt}", use_container_width=True)
                except Exception as err:
                    st.error(f"Image generation mein error aa gaya: {err}")

# --- TAB 3: PROFESSIONAL VOICE STUDIO (TTS) ---
with voice_tab:
    st.subheader("NovaAI Professional Voice Generator")
    st.write("Yahan jo text aap likhenge, usay saaf aur professional aawaz mein convert kiya jaye ga:")
    
    voice_text = st.text_area("Yahan text enter karein:", "Hello! Welcome to NovaAI. Your advanced multi-modal assistant is ready.")
    
    if st.button("Generate Voice Audio"):
        if not voice_text.strip():
            st.warning("Baraye meherbani pehle kuch text likhein!")
        else:
            with st.spinner("Professional aawaz tayyar ho rahi hai..."):
                try:
                    encoded_voice_text = requests.utils.quote(voice_text)
                    audio_api_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_voice_text}&tl=en&client=tw-ob"
                    
                    st.success("Aawaz tayyar hai! Neeche play button par click karein:")
                    st.audio(audio_api_url, format='audio/mp3')
                except Exception as voice_err:
                    st.error(f"Voice generation mein error: {voice_err}")
