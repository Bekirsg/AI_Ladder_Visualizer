# ⚙️ AI Ladder Visualizer: The PLC Copilot

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![Gemini API](https://img.shields.io/badge/AI-Google_Gemini-orange.svg)](https://ai.google.dev/)

**🌍 Canlı Demo:** [Uygulamayı Hemen Test Edin](https://ailaddervisualizer-mnpkkdd7penjzqe68sp4pg.streamlit.app/)

Doğal dil (Türkçe/İngilizce) komutlarını saniyeler içinde **IEC standartlarına uygun SCL Koduna** ve görsel **Ladder Logic** diyagramlarına dönüştüren yapay zeka tabanlı bir otomasyon asistanıdır.

![Uygulama Ekran Görüntüsü](<img width="1897" height="833" alt="image" src="https://github.com/user-attachments/assets/32496e87-cb6f-4901-ac11-09d08f665a70" />
)

## 🚀 Öne Çıkan Özellikler
* **Doğal Dil İşleme (NLP):** Karmaşık otomasyon senaryolarını anlar. (Örn: *"Konveyör bant çalışırken sensör 3 saniye kesintiye uğrarsa acil durdur."*)
* **Akıllı Validasyon (Boolean Flag):** Endüstriyel olmayan girdileri tespit eder, filtreler ve kullanıcıya düzeltme önerisi (Suggestion) sunar.
* **Anlık Görselleştirme:** Mermaid.js altyapısı ile anında Ladder diyagramı çizer.
* **State Management (Hafıza):** Session State yönetimi sayesinde sayfa yenilense dahi üretilen kodlar ve diyagramlar kaybolmaz.
* **Dışa Aktarma (Export):** Üretilen şemaları `.mmd` veya Base64 şifrelemesiyle yüksek çözünürlüklü `.png` olarak indirmenizi sağlar.

## 🛠️ Kullanılan Teknolojiler
* **AI Engine:** Google Gemini 2.5 Flash (Native JSON MIME Type & Low Temperature)
* **Frontend:** Streamlit, Streamlit-Mermaid
* **Backend:** Python 3.12
* **Deployment:** Streamlit Cloud

## 💡 Kurulum (Local Development)
Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

```bash
# Repoyu klonlayın
git clone [https://github.com/Bekirsg/AI_Ladder_Visualizer.git](https://github.com/Bekirsg/AI_Ladder_Visualizer.git)
cd AI_Ladder_Visualizer

# Sanal ortam oluşturun ve aktif edin
python -m venv venv
venv\Scripts\activate  # Windows için
# source venv/bin/activate # Mac/Linux için

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Çevresel değişkenleri ayarlayın (Kendi API anahtarınızı girin)
echo "GEMINI_API_KEY=sizin_api_anahtariniz" > .env

# Uygulamayı başlatın
streamlit run app.py
