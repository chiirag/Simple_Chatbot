from openai import OpenAI
import streamlit as st
import os

st.set_page_config(
    page_title="Chirag's Apps",  # This changes the title in the browser tab
    page_icon="🚀",               # This changes the favicon (you can also use an emoji or a file path)
    layout="wide",                # (optional) wide or centered
    initial_sidebar_state="expanded",  # (optional) expanded or collapsed
)

st.title("Chirag Jain's personal bot")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Define your system prompt here
system_prompt = "You are Chirag Jain's helpful personal assistant. Be exteremly funny and add 'Chirag thinks' when replying"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can Chirag help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="bot.png"):
        # Include the system prompt at the beginning of the message list
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": system_prompt}
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
