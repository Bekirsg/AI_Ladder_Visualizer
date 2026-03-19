import streamlit as st
import os
import json
import base64
from dotenv import load_dotenv
from google import genai
import streamlit_mermaid as stmd

# 1. Altyapı
load_dotenv()
from prompt_manager import SYSTEM_PROMPT

api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="AI Ladder Logic Visualizer", page_icon="⚙️", layout="wide")

# Sağ üst menü hafif gizle (Share butonu kalsın)
hide_st_style = """
    <style>
    header {visibility: hidden;}
    .stDeployLabel {display: none;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Başlık
st.markdown("""
    <h1 style='text-align: center; color: #00979C; font-size: 2.8rem;'>
        ⚙️ AI Ladder Logic Visualizer
    </h1>
    <p style='text-align: center; font-size: 1.2rem; color: #aaaaaa;'>
        Copilot for PLC • Doğal dilden saniyeler içinde Ladder + SCL
    </p>
""", unsafe_allow_html=True)
st.markdown("---")

# Sol Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00979C;'>🤖 AI PLC Copilot</h2>", unsafe_allow_html=True)
    
    st.markdown("👋 **Nasıl Çalışır?**")
    st.markdown("Günlük Türkçe veya İngilizce yazdığınız otomasyon senaryolarını yapay zeka ile anlar ve saniyeler içinde Ladder diyagramı + SCL kodu üretir. Yanlış veya eksik senaryolar için de yol gösterir.")
    st.markdown("---")
    
    st.header("💡 Örnek Senaryolar")
    st.markdown("**⏱️ Zamanlayıcı Testi**")
    st.code("Start butonuna basıldığında motor çalışsın. 10 saniye sonra otomatik dursun.", language="text")
    st.markdown("**🔀 Mantık Testi**")
    st.code("Tank seviyesi kritik değere ulaşırsa VE sıcaklık 50 dereceden fazlaysa soğutma valfini aç.", language="text")
    st.markdown("**🛑 Güvenlik Testi**")
    st.code("Acil stop butonuna basıldığında tüm sistemi anında durdur ve hata ışığını yak.", language="text")
    st.markdown("---")
    
    st.info("💡 **İpucu:** Daha iyi sonuçlar için 'sensör', 'valf', 'motor' gibi teknik terimleri kullanarak daha spesifik cümleler kurmanız ve yazım/noktalama hatalarını kontrol etmeniz önerilir.")
    
    st.markdown("---")
    st.markdown("⭐ **Geri Bildirim & Değerlendirme**")
    st.markdown("Hata bildirimleriniz veya geliştirme önerileriniz için aşağıdaki butonu kullanabilirsiniz.")
    st.link_button("📝 Değerlendir ve Görüş Bildir", "https://forms.gle/2rmSxXpZBjaBkuBV8")

# JSON Temizleyici - Zırhlı Versiyon
def clean_json(text):
    if not text: return "{}"
    text = text.replace("```json", "").replace("```", "").strip()
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text

# Ana Ekran
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Senaryo Girişi")
    user_input = st.text_area("Otomasyon senaryonuzu açıklayın:", height=150, placeholder="Örn: Konveyör bant çalışırken sensör 3 saniye kesintiye uğrarsa acil durdur.")
    generate_btn = st.button("🚀 Mantığı Oluştur (Generate)", use_container_width=True)

with col2:
    st.subheader("🛠️ Çıktılar")
    tab_visual, tab_code = st.tabs(["📊 Görsel Diyagram", "💻 SCL Kodu"])

if "is_generated" not in st.session_state:
    st.session_state.is_generated = False

# Core Engine
if generate_btn and user_input.strip():
    with st.spinner("Yapay zeka mantık ağını analiz ediyor..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=SYSTEM_PROMPT + f"\n\nSenaryo: {user_input}",
                config={"temperature": 0.1, "max_output_tokens": 2048, "response_mime_type": "application/json"}
            )
            
            raw_text = clean_json(response.text)
            
            # API'nin ürettiği çift ters bölüleri (\\n) JSON'ın okuyabilmesi için normalize ediyoruz
            raw_text = raw_text.replace("\\\\n", "\\n")
            
            data = json.loads(raw_text, strict=False)
            
            valid = data.get("valid", False)
            mermaid_str = data.get("mermaid", "graph LR\nA[Hata]")
            code_str = data.get("code", "// Kod üretilemedi")
            suggestion = data.get("suggestion", "")

            if valid:
                if isinstance(code_str, dict): code_str = code_str.get("SCL", str(code_str))
                
                graphbytes = mermaid_str.encode("utf8")
                base64_string = base64.b64encode(graphbytes).decode("ascii")
                png_url = f"https://mermaid.ink/img/{base64_string}"
                
                st.session_state.mermaid_str = mermaid_str
                st.session_state.code_str = code_str
                st.session_state.png_url = png_url
                st.session_state.is_generated = True
                
                st.balloons()
                st.success("✅ Harika! Mantık başarıyla derlendi.")
            else:
                st.session_state.is_generated = False
                st.warning("⚠️ Senaryo işlenirken bir pürüz çıktı.")
                if suggestion:
                    st.info(suggestion)
                else:
                    st.info("💡 Lütfen sidebar’daki örneklerden birini kopyala-yapıştır.")

        except Exception as e:
            st.session_state.is_generated = False
            if "429" in str(e) or "Quota" in str(e):
                st.warning("⏳ Sistem şu an yoğun. Lütfen 1 dakika bekleyip tekrar deneyin.")
            else:
                st.warning("⚠️ Senaryo işlenirken bir pürüz çıktı.")
                st.info("💡 **Çözüm:** Anlam bütünlüğünün korunduğundan ve yazım hatası olmadığından emin olup tekrar deneyiniz. \n Hatanın yenilenmesi halinde daha basit bir senaryo oluşturmayı deneyebilir ve örnek senaryolardan birini kullaabilirsiniz.😊")

# Çıktıları Göster
if st.session_state.is_generated:
    with tab_visual:
        # Mermaid'in sorunsuz çizmesi için kaçış karakterlerini gerçek yeni satıra dönüştürüyoruz
        final_mermaid = st.session_state.mermaid_str.replace("\\n", "\n")
        stmd.st_mermaid(final_mermaid)
        col_a, col_b = st.columns(2)
        with col_a: st.download_button("📥 Kodu İndir (.mmd)", final_mermaid, "diagram.mmd")
        with col_b: st.link_button("🖼️ PNG Olarak Görüntüle", st.session_state.png_url)
    
    with tab_code:
        st.code(st.session_state.code_str, language="pascal")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888888;'>🚀 Bekir Samet Güzlek • İTÜ Kontrol ve Otomasyon • 2026</p>", unsafe_allow_html=True)