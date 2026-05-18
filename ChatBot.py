import streamlit as st
import ollama

st.title("🤖 Chatbot Lokal Saya")

# Simpan riwayat chat agar tidak hilang
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat yang sudah lewat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari user
if prompt := st.chat_input("Halo! Mau tanya apa hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Meminta jawaban dari Ollama secara offline
    with st.chat_message("assistant"):
        response = ollama.chat(model='tinyllama', messages=[
            {'role': 'user', 'content': prompt},
        ])
        msg = response['message']['content']
        st.markdown(msg)
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
