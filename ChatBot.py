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
    
    # MASUKKAN INI KE DALAM TRY
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

except Exception as e:
    st.error(f"Gagal memuat API: {e}")
    st.stop() # Hentikan di sini agar baris 75 tidak jalan




st.title("👾 Cyb AI")
st.caption("Built with python | powered by gemini 1.5 flash")
st.caption("spesialis programming & teknologi")



for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        # Diubah ke .parts.text agar pembacaan riwayat dari Gemini SDK lebih stabil saat rerun
        st.markdown(message.parts.text)


if prompt := st.chat_input("Tanya soal teknologi/siber...")  :
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(prompt)

    
    try:
        # --- PERBAIKAN DI SINI: Menggunakan sistem streaming ---
        # Menambahkan parameter stream=True agar AI mengirim jawaban kata demi kata
        response = st.session_state.chat_session.send_message(prompt, stream=True)
        
        with st.chat_message("assistant"):
            # Fungsi pembantu untuk membaca pecahan teks (chunks) dari Google Gemini
            def chunk_generator():
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            
            # st.write_stream akan mencetak teks berjalan dan otomatis mematikan loading spinner
            st.write_stream(chunk_generator)
            
    except Exception as e:
        st.error("Terjadi masalah pada koneksi Google AI.")
        st.code(str(e))

