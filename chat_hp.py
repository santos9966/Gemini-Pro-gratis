import streamlit as st
import google.generativeai as genai

st.title("🔍 Cek Model Gemini")

try:
    # Ambil kunci dari brankas
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    st.write("Sedang menghubungi server Google...")
    
    # Minta daftar model yang tersedia
    found = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.success(f"✅ MODEL DITEMUKAN: {m.name}")
            found = True
            
    if not found:
        st.error("Tidak ada model yang ditemukan. Cek API Key Anda.")

except Exception as e:
    st.error(f"❌ ERROR API KEY: {e}")
    st.warning("Pastikan tidak ada spasi saat copy-paste API Key di Secrets.")
