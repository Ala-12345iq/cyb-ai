import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Cyb AI", page_icon="👾", layout="centered")

st.markdown("""
    <style>
    /* Mengembalikan background ke putih/terang */
    .stApp { 
        background-color: #ffffff; 
        color: #000000; 
    }
    /* Kotak chat user */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #f0f2f6;
        border-radius: 15px;
    }
    /* Kotak chat AI */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #e8f4f8;
        border-radius: 15px;
        border: 1px solid #cce5ff;
    }
    </style>
    """, unsafe_allow_html=True)

load_dotenv()

API_KEY = os.getenv("MY_API_KEY")

try:
    genai.configure(api_key=API_KEY)
    
    # 1. Inisialisasi Model Utama (Gemini 2.5) - Spasi sudah disamakan
    if "chat_session" not in st.session_state:
        model_utama = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            system_instruction="Kamu adalah Tech-Guard AI. Hanya bantu soal teknologi."
        )
        st.session_state.chat_session = model_utama.start_chat(history=[])
        
    # 2. Inisialisasi Model Cadangan (Gemini 3.1) - Spasi sudah disamakan
    if "chat_session_backup" not in st.session_state:
        model_cadangan = genai.GenerativeModel(
            model_name="models/gemini-3.1-flash-lite",
            system_instruction="Kamu adalah Tech-Guard AI. Hanya bantu soal teknologi."
        )
        st.session_state.chat_session_backup = model_cadangan.start_chat(history=[])

    if "messages" not in st.session_state:
        st.session_state.messages = []

except Exception as e:
    st.error(f"Gagal memuat API: {e}")
    st.stop() 


st.title("👾 Cyb AI")
st.caption("Built with python | powered by gemini 2.5 flash")
st.caption("spesialis programming & teknologi")


# Membaca riwayat pesan dari state lokal Streamlit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Tanya soal teknologi/siber..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            try:
                # Mencoba jalur utama menggunakan model 2.5
                response_stream = st.session_state.chat_session.send_message(prompt, stream=True)
                
                def chunk_generator():
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text
                full_response = st.write_stream(chunk_generator())
                
            except Exception as api_error:
                # Mengalihkan ke cadangan gratis 3.1 jika jalur utama 503 (Penuh)
                if "503" in str(api_error):
                    st.warning("⚠️ Server utama penuh. Beralih ke server cadangan...")
                    response_stream_backup = st.session_state.chat_session_backup.send_message(prompt, stream=True)
                    
                    def chunk_generator_backup():
                        for chunk in response_stream_backup:
                            if chunk.text:
                                yield chunk.text
                    full_response = st.write_stream(chunk_generator_backup())
                else:
                    raise api_error
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        st.error("Terjadi masalah pada koneksi Google AI.")
        st.code(str(e))
