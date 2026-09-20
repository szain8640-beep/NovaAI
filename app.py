import streamlit as st
import os
import requests
from groq import Groq

# Page Config
st.set_page_config(page_title="NovaAI Pro Studio", page_icon="🤖", layout="centered")

st.title("🤖 NovaAI - Professional Multi-Modal Studio")
st.write("NovaAI ka mukammal aur naya version live ho chuka hai!")

# Tabs
chat_tab, image_tab, voice_tab = st.tabs(["💬 Smart Chat", "🖼️ AI Image Generator", "🗣️ Voice Studio"])

# 1. CHAT TAB
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
            {"role": "assistant", "content": "Salam! Main NovaAI hoon. Aap mujhse koi bhi sawal pooch sakte hain!"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("NovaAI se kuch bhi puchein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if api_key:
                try:
                    client = Groq(api_key=api_key)
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[{"role": "system", "content": "You are NovaAI."}] + st.session_state.messages,
                        temperature=0.7,
                    )
                    reply = completion.choices[0].message.content
                except Exception as e:
                    reply = f"Error: {e}"
            else:
                reply = f"Aapne kaha: '{prompt}'. NovaAI smart chat active hai!"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

# 2. IMAGE TAB
with image_tab:
    st.subheader("NovaAI Image Studio")
    img_prompt = st.text_input("Tasveer ke liye prompt likhein:", "A futuristic sci-fi city")
    if st.button("Generate Image"):
        if img_prompt:
            with st.spinner("Generating image..."):
                encoded = requests.utils.quote(img_prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded}"
                st.success("Tasveer tayyar hai!")
                st.image(img_url, caption=img_prompt, use_container_width=True)

# 3. VOICE TAB
with voice_tab:
    st.subheader("NovaAI Voice Studio")
    v_text = st.text_area("Text likhein jo sunna chahte hain:", "Hello! Welcome to NovaAI.")
    if st.button("Generate Voice"):
        if v_text:
            with st.spinner("Generating audio..."):
                encoded_v = requests.utils.quote(v_text)
                audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_v}&tl=en&client=tw-ob"
                st.success("Aawaz tayyar hai!")
                st.audio(audio_url, format='audio/mp3')
