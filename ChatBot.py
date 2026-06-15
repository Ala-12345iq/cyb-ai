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
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Kamu adalah Tech-Guard AI. Hanya bantu soal teknologi."
    )
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

except Exception as e:
    st.error(f"Gagal memuat API: {e}")
    st.stop() 

st.title("👾 Cyb AI")
st.caption("Built with python | powered by gemini 1.5 flash")
st.caption("spesialis programming & teknologi")

# --- PERBAIKAN DI SINI ---
# Menggunakan pengecekan yang lebih aman untuk mengambil teks dari komponen parts
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        # Ambil text menggunakan atribut .text dari element parts yang ada
        if message.parts:
            st.markdown(message.parts[0].text)

if prompt := st.chat_input("Tanya soal teknologi/siber..."):
    # Tampilkan pesan user langsung di layar
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Kirim ke API Gemini
        response = st.session_state.chat_session.send_message(prompt)
        # Tampilkan respon AI langsung di layar
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error("Terjadi masalah pada koneksi Google AI.")
        st.code(str(e))

