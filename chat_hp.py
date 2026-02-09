import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Gemini 2.5 Flash", page_icon="⚡")
st.title("⚡ Gemini 2.5 Flash")

# --- SETUP API KEY ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Kunci Rahasia belum dipasang di Settings -> Secrets")
    st.stop()

# --- SETUP MODEL (MENGGUNAKAN GEMINI 2.5) ---
# Kita pakai model yang SUDAH PASTI ADA di daftar Anda
model = genai.GenerativeModel('gemini-2.5-flash')

# --- LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Tampilkan Chat Lama (History)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 2. Input User (Kotak Ketik)
if prompt := st.chat_input("Tanya apa saja..."):
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Respon Robot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Kirim ke Google
            # Kita kirim history chat agar dia ingat konteks
            chat_history = []
            for msg in st.session_state.messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})
            
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt)
            
            # Tampilkan Jawaban
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Simpan ke memori
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
