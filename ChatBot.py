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
        system_instruction="Kamu adalah Tech-Guard AI. Hanya bantu soal teknologi. Tolak dengan sopan jika ditanya di luar topik teknologi."
    )
    
    # Inisialisasi backend chat session Gemini
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        
    # PERBAIKAN UTAMA: Gunakan session_state mandiri khusus untuk rendering UI Streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = []

except Exception as e:
    st.error(f"Gagal memuat API: {e}")
    st.stop() 

st.title("👾 Cyb AI")
st.caption("Built with python | powered by gemini 1.5 flash")
st.caption("spesialis programming & teknologi")

# 1. Menampilkan seluruh riwayat chat yang tersimpan di memori Streamlit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Logika Input Pesan dari Pengguna
if prompt := st.chat_input("Tanya soal teknologi/siber..."):
    
    # Tampilkan pesan user secara instan di layar
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Simpan pesan user ke dalam riwayat UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Panggil API Gemini di dalam animasi spinner komponen assistant
    with st.chat_message("assistant"):
        with st.spinner("Cyb AI sedang berpikir..."):
            try:
                # Kirim pesan ke API
                response = st.session_state.chat_session.send_message(prompt)
                ai_response = response.text
                
                # Tampilkan respon AI secara instan di layar setelah loading selesai
                st.markdown(ai_response)
                
                # Simpan respon AI ke dalam riwayat UI
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error("Terjadi masalah pada koneksi Google AI.")
                st.code(str(e))
