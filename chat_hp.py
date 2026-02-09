import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Gemini Jumbo", page_icon="⚡")

# --- 2. TRIK MEMPERBESAR TULISAN (CSS) ---
# Ini codingan khusus supaya tulisan di HP jadi besar
st.markdown("""
<style>
    /* Ubah ukuran huruf chat menjadi 20px (lebih besar) */
    .stChatMessage .stMarkdown p {
        font-size: 20px !important;
        line-height: 1.6 !important;
    }
    
    /* Ubah ukuran huruf di kotak ketik bawah */
    .stChatInput textarea {
        font-size: 18px !important;
    }
    
    /* Ubah tombol kirim jadi lebih jelas */
    .stChatInput button {
        background-color: #FF4B4B;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Gemini 2.5 Flash")

# --- 3. SETUP API KEY ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Kunci Rahasia belum dipasang di Settings -> Secrets")
    st.stop()

# --- 4. MEMILIH MODEL ---
# Jika ingin ganti model, ubah tulisan di dalam kurung ini
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 5. LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat Lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input User
if prompt := st.chat_input("Tanya apa saja..."):
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Respon Robot
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            chat_history = []
            for msg in st.session_state.messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})
            
            # Streaming (Agar teks muncul ketik per kata, lebih keren)
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
