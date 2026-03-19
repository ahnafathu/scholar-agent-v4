import requests
import json
import time
from ddgs import DDGS # Versi terbaru sesuai warning tadi
from bs4 import BeautifulSoup

# 1. KONFIGURASI
API_KEY = "AIzaSyCQ7u9aRscVl44sLJnokW-sc7ti71EYxdA"
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200: return ""
        soup = BeautifulSoup(res.text, 'html.parser')
        for s in soup(['script', 'style', 'nav', 'footer']): s.decompose()
        text = soup.get_text(" ", strip=True)
        return text[:4000] 
    except:
        return ""

def analyze_scholarship(data_list, user_query):
    print("\n--- AI Sedang Merumus Laporan Khusus Untuk Anda... ---")
    combined_data = "\n---\n".join(data_list)
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"DATA INTERNET:\n{combined_data}\n\nPERMINTAAN USER: {user_query}\n\nTUGAS: Berikan daftar beasiswa yang paling relevan. Sertakan Nama, Link, dan Deadline. Jika ada info soal syarat bahasa (IELTS/TOEFL), tonjolkan itu. Jawab dengan gaya Advisor yang tegas dan informatif."
            }]
        }]
    }
    res = requests.post(URL_API, headers={'Content-Type': 'application/json'}, data=json.dumps(prompt))
    return res.json()['candidates'][0]['content']['parts'][0]['text'] if res.status_code == 200 else "API Error"

# ==========================================================
# ANTARMUKA INTERAKTIF (KOLOM TANYA)
# ==========================================================
print("\n" + "="*50)
print("       🤖 SCHOLAR AGENT LAB - INTERACTIVE MODE")
print("="*50)

# Di sini 'kolom tanya' nya, Naf!
negara = input("📍 Mau cari beasiswa di negara mana? (Contoh: Taiwan/Jepang): ")
jurusan = input("🎓 Jurusan apa yang lo minati? (Contoh: Computer Science): ")
jenjang = input("🏫 Jenjang apa? (Contoh: S1/S2): ")

user_query = f"Beasiswa {jenjang} {jurusan} di {negara} 2025 2026"
query_search = f"scholarship {jenjang} {jurusan} {negara} 2025 2026 for indonesian students"

print(f"\n🚀 Agent meluncur mencari: {user_query}...")

# --- PROSES SEARCHING ---
raw_contents = []
with DDGS() as ddgs:
    results = list(ddgs.text(query_search, max_results=5))
    
    for i, r in enumerate(results):
        link = r['href']
        print(f"[{i+1}] Membuka link: {link}")
        text = get_content(link)
        if text:
            raw_contents.append(f"SUMBER: {link}\nKONTEN: {text}")
        time.sleep(1)

# --- OUTPUT FINAL ---
if raw_contents:
    print("\n" + "X"*50 + "\nHASIL ANALISIS LAB:\n" + "X"*50)
    laporan = analyze_scholarship(raw_contents, user_query)
    print(laporan)
else:
    print("\n❌ Gagal dapet data. Coba ganti kata kunci lo, Naf.")