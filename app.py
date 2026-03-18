import streamlit as st
import os
import json
import base64
from dotenv import load_dotenv
from google import genai
import streamlit_mermaid as stmd

# 1. Altyapı ve Güvenli API Yönetimi
load_dotenv()
from prompt_manager import SYSTEM_PROMPT

# Streamlit Cloud (st.secrets) veya Lokal (.env) kontrolü
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Ladder Logic Visualizer", page_icon="⚙️", layout="wide")

# 2. Viral Frontend Tasarımı
st.markdown("""
    <h1 style='text-align: center; color: #00979C; font-size: 2.8rem;'>
        ⚙️ AI Ladder Logic Visualizer
    </h1>
    <p style='text-align: center; font-size: 1.2rem; color: #aaaaaa;'>
        Copilot for PLC • Doğal dilden saniyeler içinde Ladder + SCL
    </p>
""", unsafe_allow_html=True)
st.markdown("---")

# Sol Menü (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00979C;'>🤖 AI PLC</h2>", unsafe_allow_html=True)
    st.header("💡 Örnek Senaryolar")
    st.markdown("**⏱️ Zamanlayıcı Testi**")
    st.code("Start butonuna basıldığında motor çalışsın. 10 saniye sonra otomatik dursun.", language="text")
    st.markdown("**🔀 Mantık (AND/OR) Testi**")
    st.code("Tank seviyesi kritik değere ulaşırsa VE sıcaklık 50 dereceden fazlaysa soğutma valfini aç.", language="text")
    st.markdown("**🛑 Güvenlik Testi**")
    st.code("Acil stop butonuna basıldığında tüm sistemi anında durdur ve hata ışığını yak.", language="text")
    st.markdown("---")
    st.info("Sistemin halüsinasyon görmemesi için cümlelerinizi spesifik tutun.")

# 3. JSON Temizleyici
def clean_json(text):
    text = text.replace("```json", "").replace("```", "").strip()
    return text

# 4. Ana Ekran
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Senaryo Girişi")
    user_input = st.text_area(
        "Otomasyon senaryonuzu açıklayın:", 
        height=150,
        placeholder="Örn: Konveyör bant çalışırken sensör 3 saniye kesintiye uğrarsa acil durdur."
    )
    generate_btn = st.button("🚀 Mantığı Oluştur (Generate)", use_container_width=True)

with col2:
    st.subheader("🛠️ Çıktılar")
    tab_visual, tab_code = st.tabs(["📊 Görsel Diyagram", "💻 SCL Kodu"])

# 5. Core Engine
# 5. Core Engine (Hafıza ve State Yönetimi)
if "is_generated" not in st.session_state:
    st.session_state.is_generated = False

if generate_btn and user_input.strip():
    with st.spinner("Yapay zeka mantık ağını analiz ediyor. Lütfen bekleyin..."):
                    try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=SYSTEM_PROMPT + f"\n\nSenaryo: {user_input}",
                config={
                    "temperature": 0.1,
                    "max_output_tokens": 2048,
                    "response_mime_type": "application/json"
                }
            )
            
            raw_text = clean_json(response.text)
            data = json.loads(raw_text)
            
            valid = data.get("valid", False)
            mermaid_str = data.get("mermaid", "graph LR\nA[Hata]")
            code_str = data.get("code", "// Kod üretilemedi")
            suggestion = data.get("suggestion", "")

            if valid:
                # Başarılı yol
                st.session_state.mermaid_str = mermaid_str
                st.session_state.code_str = code_str
                st.session_state.is_generated = True
                st.balloons()
                st.success("✅ Mantık başarıyla derlendi!")
            else:
                # Geçersiz yol - başarı mesajı YOK
                st.session_state.is_generated = False
                st.warning("⚠️ Bu senaryo anlaşılmadı veya PLC mantığına uymuyor.")
                if suggestion:
                    st.info(f"💡 Öneri: {suggestion}")
                st.info("Tekrar deneyin veya sidebar’daki örneklerden birini kopyalayın.")

        except json.JSONDecodeError:
            st.session_state.is_generated = False
            st.warning("⚠️ AI JSON formatında cevap veremedi. Cümleyi biraz daha net yazın.")
        except Exception as e:
            st.session_state.is_generated = False
            st.error(f"🚨 Beklenmeyen hata: {str(e)[:120]}")
# Alt Bilgi (Footer)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888888;'>🚀 Bekir Samet Güzlek • İTÜ Kontrol ve Otomasyon • 2026</p>", unsafe_allow_html=True)