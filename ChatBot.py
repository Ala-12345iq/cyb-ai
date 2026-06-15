import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Konfigurasi Halaman & Gaya Tampilan (CSS Kustom Anda)
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

# 2. Memuat Environment Variables dari file murni .env
load_dotenv()
API_KEY = os.getenv("MY_API_KEY")

# 3. Proteksi Awal: Jika API Key kosong, hentikan aplikasi agar tidak crash/infinite loading
if not API_KEY:
    st.error("🚨 Kritis: API Key tidak ditemukan! Pastikan file Anda bernama murni '.env' (bukan '.env.txt') dan berisi variabel MY_API_KEY")
    st.stop()

# 4. Inisialisasi Model & Service Chat ke dalam Session State (Hanya dijalankan 1x di awal)
try:
    genai.configure(api_key=API_KEY)
    
    # Simpan objek model ke state agar tidak di-recreate setiap user mengetik
    if "gemini_model" not in st.session_state:
        st.session_state.gemini_model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",  # Menggunakan prefiks 'models/' untuk mencegah error 404
            system_instruction="Kamu adalah Tech-Guard AI. Hanya bantu soal teknologi. Tolak dengan sopan jika ditanya di luar topik teknologi."
        )
    
    # Inisialisasi backend chat session Gemini
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = st.session_state.gemini_model.start_chat(history=[])
        
    # Inisialisasi memori riwayat chat khusus untuk render UI Streamlit (Anti-Layar Kosong)
    if "messages" not in st.session_state:
        st.session_state.messages = []

except Exception as e:
    st.error(f"Gagal memuat API atau Inisialisasi Model: {e}")
    st.stop() 

# 5. Desain Komponen Header
st.title("👾 Cyb AI")
st.caption("Built with python | powered by gemini 1.5 flash")
st.caption("spesialis programming & teknologi")

# 6. Render Riwayat Chat dari State Lokal Streamlit
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Logika Input Chat & Pengiriman Pesan ke Model Service
if prompt := st.chat_input("Tanya soal teknologi/siber..."):
    
    # Tampilkan pesan user secara instan di layar
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Simpan pesan user ke dalam memori lokal UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Panggil Service Chat dari Gemini di dalam blok visual Assistant
    with st.chat_message("assistant"):
        with st.spinner("Cyb AI sedang berpikir..."):
            try:
                # Menggunakan stream=True untuk mengirim respons kata demi kata (Anti-Hang)
                response_stream = st.session_state.chat_session.send_message(prompt, stream=True)
                
                # Fungsi pembantu generator untuk membaca pecahan teks dari server Google
                def chunk_generator():
                    for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text
                
                # st.write_stream akan mencetak teks berjalan secara real-time
                # Efek spinner otomatis mati begitu huruf pertama dicetak (Anti-Infinite Loading)
                full_response = st.write_stream(chunk_generator())
                
                # Simpan jawaban akhir AI ke memori lokal UI setelah streaming selesai
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error("Terjadi masalah pada koneksi Google AI.")
                st.code(str(e))
