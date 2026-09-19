import streamlit as st
import os
from groq import Groq
import requests

# Page Config
st.set_page_config(page_title="NovaAI Studio", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 NovaAI - Multi-Modal Studio")
st.write("Aapka apna advanced AI platform!")

# Using Tabs so options are directly visible on screen!
chat_tab, image_tab = st.tabs(["💬 Text Chat", "🖼️ AI Image Generator"])

# Initialize Groq Client for Text Chat
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        pass

if not api_key:
    st.error("Groq API Key missing! Please set it in Streamlit Secrets.")
else:
    client = Groq(api_key=api_key)

    with chat_tab:
        st.subheader("NovaAI Smart Chat")
        
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

    with image_tab:
        st.subheader("NovaAI Image Studio")
        st.write("Yahan aap apni pasand ki tasveer ka text likhein:")
        
        user_image_prompt = st.text_input("Misal: A beautiful sunset over mountains in Pakistan", "", key="img_prompt_input")
        
        if st.button("Generate Image"):
            if not user_image_prompt.strip():
                st.warning("Pehle koi prompt likhein!")
            else:
                with st.spinner("Tasveer generate ho rahi hai, baraye meherbani intezar karein..."):
                    try:
                        encoded_prompt = requests.utils.quote(user_image_prompt)
                        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                        
                        st.success("Tasveer kamyabi ke sath ban gayi hai!")
                        st.image(image_url, caption=user_image_prompt, use_column_width=True)
                    except Exception as err:
                        st.error(f"Image generation mein error aa gaya: {err}")
