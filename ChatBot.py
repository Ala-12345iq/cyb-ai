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
    
    
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    
    model_tujuan = ""
    for m in available_models:
        if "gemini-1.5-flash" in m:
            model_tujuan = m
            break
    if not model_tujuan:
        model_tujuan = available_models[0] 

    st.info(f"🚀 AI Aktif menggunakan model: {model_tujuan}")

    model = genai.GenerativeModel(
        model_name=model_tujuan,
        system_instruction=(
            "Kamu adalah Tech-Guard AI. Hanya bantu soal teknologi. "
            "Jika di luar itu, jawab: 'Maaf, saya spesialis teknologi saja.'"
        )
    )
except Exception as e:
    st.error(f"Gagal memuat API: {e}")



st.title("👾 Cyb AI")
st.caption("Built with python | powered by gemini 2.5 flash")
st.caption("spesialis programming & teknologi")


if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)


if prompt := st.chat_input("Tanya soal teknologi/siber...")  :
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(prompt)

    
    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        st.error("Terjadi masalah pada koneksi Google AI.")
        st.code(str(e))