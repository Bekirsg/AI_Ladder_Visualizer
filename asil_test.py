import os
from dotenv import load_dotenv
from google import genai

# Şifreyi yüklüyoruz
load_dotenv()

print("Sistem devrede. API test ediliyor. Lütfen bekleyin...")

try:
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Bana sadece su JSON metnini dondur: {'durum': 'harika'}"
    )
    print("\n--- API YANITI GELDİ ---")
    print(response.text)
except Exception as e:
    print("\nHATA VAR:", e)