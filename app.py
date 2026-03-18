import streamlit as st
import os
import json
from dotenv import load_dotenv
from google import genai
import streamlit_mermaid as stmd

# 1. Altyapı Hazırlığı
load_dotenv()
client = genai.Client()

st.set_page_config(page_title="AI Ladder Logic Visualizer", page_icon="⚙️", layout="wide")

# 2. Sol Menü (Sidebar) - YENİ EKLENEN VİTRİN
with st.sidebar:
    st.header("💡 Örnek Senaryolar")
    st.markdown("Aşağıdaki komutları kopyalayarak sistemi hemen test edebilirsiniz:")
    
    st.markdown("**⏱️ Zamanlayıcı Testi**")
    st.code("Start butonuna basıldığında motor çalışsın. 10 saniye sonra otomatik dursun.", language="text")
    
    st.markdown("**🔀 Mantık (AND/OR) Testi**")
    st.code("Tank seviyesi kritik değere ulaşırsa VE sıcaklık 50 dereceden fazlaysa soğutma valfini aç.", language="text")
    
    st.markdown("**🛑 Güvenlik Testi**")
    st.code("Acil stop (E-Stop) butonuna basıldığında tüm sistemi anında durdur ve hata ışığını yak.", language="text")
    
    st.markdown("---")
    st.info("ℹ️ İpucu: Sistemin halüsinasyon görmemesi için cümlelerinizi endüstriyel standartlara uygun, net ve spesifik tutun.")

# 3. Çekirdek Algoritma (Sıfır Hata Toleranslı Prompt)
SYSTEM_PROMPT = """Sen kıdemli bir PLC ve Otomasyon mühendisisin.
Kullanıcının verdiği senaryoyu AL ve SADECE aşağıdaki formatta JSON üret:
{
  "mermaid": "graph LR\\n A[Input] --> B[Timer]\\n B --> C[Motor]",
  "code": "SCL KODU BURAYA"
}
KRİTİK KURALLAR:
1. 'mermaid' kodu 'graph LR' ile başlamalı. Node (düğüm) isimlerinde ASLA Türkçe karakter (ş, ç, ö, ü, ğ, ı), boşluk veya özel karakter kullanma! (Örn: C[Motor_Calisiyor] kullan, C[Motor Çalışıyor] KULLANMA).
2. 'code' sadece düz metin (string) SCL kodudur. İçiçe JSON yapma.
3. JSON dışında tek kelime açıklama yapma."""

# 4. JSON Temizleyici
def clean_json(text):
    text = text.replace("```json", "").replace("```", "").strip()
    return text

# 5. Frontend (Ana Ekran) Tasarımı
st.title("⚙️ AI Ladder Logic Visualizer")
st.markdown("**Copilot for PLC:** Doğal dil komutlarını anında Ladder (Mermaid) ve SCL koduna çevirin.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Senaryo Girişi")
    user_input = st.text_area(
        "Otomasyon senaryonuzu açıklayın:", 
        height=150,
        placeholder="Sol menüdeki (Sidebar) örnek senaryolardan birini buraya yapıştırıp test edebilirsiniz."
    )
    generate_btn = st.button("🚀 Mantığı Oluştur (Generate)", use_container_width=True)

with col2:
    st.subheader("🛠️ Çıktılar")
    tab_visual, tab_code = st.tabs(["📊 Görsel Diyagram (Mermaid)", "💻 SCL/Python Kodu"])

# 6. Butona Basıldığında Olacaklar
if generate_btn and user_input.strip():
    with st.spinner("Yapay zeka mantık ağını analiz ediyor. Lütfen bekleyin..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=SYSTEM_PROMPT + f"\n\nSenaryo: {user_input}"
            )
            
            raw_text = clean_json(response.text)
            data = json.loads(raw_text)
            
            mermaid_str = data.get("mermaid", "graph LR\nA[Hata]")
            mermaid_str = mermaid_str.replace("```mermaid", "").replace("```", "").strip()
            
            code_str = data.get("code", "// Kod üretilemedi")
            if isinstance(code_str, dict):
                code_str = code_str.get("SCL", str(code_str))
            
            with tab_visual:
                stmd.st_mermaid(mermaid_str)
                st.caption("🔍 Üretilen Mermaid Kodu (Arka Plan):")
                st.code(mermaid_str, language="mermaid")
            
            with tab_code:
                st.code(code_str, language="pascal")
                
            st.success("✅ İşlem başarıyla tamamlandı!")
                
        except Exception as e:
            st.error("Sistem çıktıyı işlerken bir hata ile karşılaştı.")
            st.error(f"Teknik Detay: {e}")