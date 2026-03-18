# ⚙️ AI Ladder Logic Visualizer (Copilot for PLC)

Doğal dil komutlarını saniyeler içinde endüstriyel PLC mantığına (Ladder Diagram) ve SCL koduna çeviren yapay zeka destekli bir otomasyon asistanıdır.

## 🚀 Projenin Amacı
Otomasyon mühendislerinin mantık hatalarını kodlamadan önce görselleştirmesini sağlamak ve "Copilot for PLC" konseptini hayata geçirmektir. Sistem, Gemini AI gücünü kullanarak karmaşık senaryoları anında test edilebilir algoritmalara dönüştürür.

## 🛠️ Kullanılan Teknolojiler
* **Yapay Zeka:** Google Gemini 2.5 Flash API
* **Arayüz (Frontend):** Streamlit 
* **Görselleştirme:** Mermaid.js 

## 💻 Nasıl Çalışır?
Kullanıcı senaryoyu girer (Örn: "Start butonuna basıldığında motor çalışsın. 10 saniye sonra otomatik dursun."). Sistem saniyeler içinde hatasız bir JSON çıktısı üretir ve bunu ekranda akış diyagramı ile IEC standartlarına uygun SCL kodu olarak görselleştirir.