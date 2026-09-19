import streamlit as st
from groq import Groq

st.set_page_config(page_title="NovaAI - Global Assistant", page_icon="🤖")

st.title("🤖 NovaAI")
st.write("Aapka apna advanced AI assistant jo Computer Science, Coding, aur har field mein aapki madad ke liye tayyar hai!")

client = Groq(api_key="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")

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
            "content": "Aap ek expert, highly intelligent aur dostana AI assistant hain jiska naam NovaAI hai. Aap computer science, coding, aur dunya bhar ki har information ke expert hain."
        }
        
        full_messages = [system_prompt] + st.session_state.messages

        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=full_messages,
                temperature=0.7
            )
            bot_reply = response.choices[0].message.content
        except Exception as e:
            bot_reply = f"Maazrat, koi error aa gaya hai: {e}"

        message_placeholder.markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
