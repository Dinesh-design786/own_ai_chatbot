# Refactored for openai>=1.0.0
import streamlit as st
from openai import OpenAI

# Setup OpenAI client
client = None

with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    else:
        user_api_key = st.text_input('Enter OpenAI API token:', type='password')
        if user_api_key:
            if user_api_key.startswith('sk-') and len(user_api_key) > 40:
                st.success('Proceed to entering your prompt message!', icon='👉')
                client = OpenAI(api_key=user_api_key)
            else:
                st.warning('Please enter a valid OpenAI API key!', icon='⚠️')

if client:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Get streamed response
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                full_response += content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.warning("Please provide a valid OpenAI API key in the sidebar to continue.")
