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

# --- PERBAIKAN 1: Sinkronisasi Tampilan dengan Role API ---
# Gemini API menyimpan role dengan nama 'user' dan 'model'
for message in st.session_state.chat_session.history:
    # Ubah 'model' milik Gemini menjadi 'assistant' agar CSS Streamlit Anda aktif
    streamlit_role = "user" if message.role == "user" else "assistant"
    with st.chat_message(streamlit_role):
        # Cara paling aman mengambil string teks murni dari SDK Gemini terbaru
        if hasattr(message, "parts") and message.parts:
            st.markdown(message.parts[0].text)

# --- PERBAIKAN 2: Penanganan Alur Kirim Pesan ---
if prompt := st.chat_input("Tanya soal teknologi/siber..."):
    # Tampilkan chat pengguna secara real-time
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Tampilkan animasi loading selagi menunggu server Google merespons
        with st.chat_message("assistant"):
            with st.spinner("Cyb AI sedang mengetik..."):
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                
        # Memaksa Streamlit untuk menyimpan state dengan benar setelah update history
        st.rerun()
                
    except Exception as e:
        st.error("Terjadi masalah pada koneksi Google AI.")
        st.code(str(e))

