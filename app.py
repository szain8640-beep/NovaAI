import streamlit as st
import os
from groq import Groq
import requests
from gtts import gTTS
import io

# Page Config
st.set_page_config(page_title="NovaAI Studio", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 NovaAI - Advanced Multi-Modal Studio")
st.write("Aapka apna mukammal AI platform (Text Chat, Image Generation, aur Voice Speech ke sath)!")

# Tabs for all features
chat_tab, image_tab, voice_tab = st.tabs(["💬 Text Chat", "🖼️ AI Image Generator", "🗣️ Voice Generator (TTS)"])

# --- TAB 1: TEXT CHAT ---
with chat_tab:
    st.subheader("NovaAI Smart Chat")
    
    # Apni Groq API Key yahan enter karein
    api_key = "YOUR_GROQ_API_KEY_YAHAN_LIKHEIN"
    
    if api_key == "YOUR_GROQ_API_KEY_YAHAN_LIKHEIN":
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            api_key = os.environ.get("GROQ_API_KEY")

    if not api_key or api_key == "YOUR_GROQ_API_KEY_YAHAN_LIKHEIN":
        st.warning("⚠️ Baraye meherbani code mein apni Groq API Key enter karein taake chat chal sake.")
    else:
        client = Groq(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("NovaAI se kuch bhi puchein..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                system_prompt = {
                    "role": "system",
                    "content": "Aap ek expert, highly intelligent aur dostana AI assistant hain jiska naam NovaAI hai."
                }
                full_messages = [system_prompt] + st.session_state.messages

                try:
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=full_messages,
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    bot_reply = completion.choices[0].message.content
                except Exception as e:
                    bot_reply = f"Maazrat, koi error aa gaya hai: {e}"

                message_placeholder.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# --- TAB 2: AI IMAGE GENERATOR ---
with image_tab:
    st.subheader("NovaAI Image Studio")
    st.write("Yahan apni pasand ki tasveer ka text likhein:")
    
    user_image_prompt = st.text_input("Misal: A beautiful realistic portrait of a handsome boy", "", key="img_prompt_input")
    
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
                    st.error(f"Image generation mein error aa gaya: {err}")

# --- TAB 3: VOICE GENERATOR (TEXT-TO-SPEECH) ---
with voice_tab:
    st.subheader("NovaAI Voice Studio")
    st.write("Jo text aap likhenge, NovaAI usay aawaz (audio) mein badal dega:")
    
    voice_text = st.text_area("Yahan text likhein jo aap sunna chahte hain:", "Hello! Main NovaAI hoon, aapka apna advanced AI assistant.")
    
    if st.button("Generate Voice Audio"):
        if not voice_text.strip():
            st.warning("Pehle kuch text likhein!")
        else:
            with st.spinner("Aawaz tayyar ho rahi hai..."):
                try:
                    # Convert text to speech using gTTS
                    tts = gTTS(text=voice_text, lang='en')
                    audio_fp = io.BytesIO()
                    tts.write_to_fp(audio_fp)
                    audio_fp.seek(0)
                    
                    st.success("Aawaz kamyabi ke sath tayyar ho gayi hai!")
                    st.audio(audio_fp, format='audio/mp3')
                except Exception as voice_err:
                    st.error(f"Voice generation mein error: {voice_err}")
