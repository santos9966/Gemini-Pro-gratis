import streamlit as st
import google.generativeai as genai
import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Gemini Jumbo", page_icon="⚡")

# --- 2. CSS KHUSUS (TULISAN JUMBO) ---
st.markdown("""
<style>
    /* 1. Memperbesar tulisan Chat Robot & User (24px) */
    .stChatMessage .stMarkdown p {
        font-size: 24px !important;
        line-height: 1.5 !important;
    }
    
    /* 2. Memperbesar tulisan saat MENGETIK (Input Area) */
    .stChatInput textarea {
        font-size: 24px !important; 
        line-height: 1.5 !important;
        height: 80px !important; /* Kotak lebih tinggi */
    }
    
    /* 3. Memperbesar Tombol Kirim */
    .stChatInput button {
        width: 3rem !important;
        height: 3rem !important;
    }
    
    /* 4. Judul Atas */
    h1 {
        font-size: 32px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- JUDUL ---
st.title("⚡ Gemini 2.5 Flash")

# --- 3. SETUP API KEY ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Kunci Rahasia belum dipasang.")
    st.stop()

# --- 4. PILIH MODEL (Gunakan yang tersedia di akun Anda) ---
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 5. LOGIKA CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat Lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. FITUR SIMPAN CHAT (SIDEBAR) ---
with st.sidebar:
    st.header("🗄️ Menu")
    if st.button("🗑️ Hapus Chat (Reset)"):
        st.session_state.messages = []
        st.rerun()
    
    # Persiapkan teks untuk didownload
    chat_text = ""
    for msg in st.session_state.messages:
        role = "SAYA" if msg["role"] == "user" else "ROBOT"
        chat_text += f"{role}: {msg['content']}\n\n"
        
    # Tombol Download
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    st.download_button(
        label="💾 Download/Simpan Chat",
        data=chat_text,
        file_name=f"Chat_Gemini_{timestamp}.txt",
        mime="text/plain"
    )

# --- 7. INPUT USER ---
if prompt := st.chat_input("Ketik di sini..."):
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
            
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
