import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Gemini Pro", page_icon="🤖")
st.title("🤖 Gemini Pro Pribadi")

# Ambil API Key dari Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Key belum dipasang di Secrets!")
    st.stop()

# Inisialisasi Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Inisialisasi Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat Lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input User
if prompt := st.chat_input("Tanya sesuatu..."):
    # Tampilkan pesan user
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Respon Robot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Kirim chat ke Google
            # Kita buat history chat sederhana
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            message_placeholder.error(f"Error: {e}")



