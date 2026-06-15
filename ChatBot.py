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
        model_name="models/gemini-1.5-flash",
        system_instruction="Kamu adalah Tech-Guard AI. Hanya bantu soal teknologi. Tolak topik lain dengan sopan."
    )
    
    # 1. KUNCI ANTI-GAGAL: Membuat dua penyimpanan state yang terpisah
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        
    if "messages" not in st.session_state:
        st.session_state.messages = []

except Exception as e:
    st.error(f"Gagal memuat API: {e}")
    st.stop() # Hentikan di sini agar baris di bawah tidak jalan

st.title("👾 Cyb AI")
st.caption("Built with python | powered by gemini 1.5 flash")
st.caption("spesialis programming & teknologi")

# 2. KUNCI ANTI-GAGAL: Membaca riwayat dari state lokal Streamlit (bukan dari API Google)
# Cara ini menjamin balon chat lama Anda tidak akan pernah hilang atau blank saat halaman rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya soal teknologi/siber..."):
    # Tampilkan pesan user secara instan di layar
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Simpan pesan user ke riwayat lokal
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        # Tampilkan balon chat asisten beserta animasi spinner
        with st.chat_message("assistant"):
            with st.spinner("Cyb AI sedang berpikir..."):
                # 3. KUNCI ANTI-GAGAL: Mengaktifkan stream=True agar data dicicil per kata
                response_stream = st.session_state.chat_session.send_message(prompt, stream=True)
                
                # Fungsi pembantu untuk membaca pecahan teks (chunks) dari Google Gemini
                def chunk_generator():
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text
                
                # st.write_stream akan mencetak efek teks berjalan secara real-time
                # Spinner akan otomatis hancur begitu huruf pertama muncul (Anti-Infinite Loading)
                full_response = st.write_stream(chunk_generator())
        
        # Simpan jawaban lengkap AI ke riwayat lokal setelah streaming selesai
        st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        st.error("Terjadi masalah pada koneksi Google AI.")
        st.code(str(e))
