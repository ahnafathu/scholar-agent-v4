import requests
import json
import time
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

API_KEY = "AIzaSyCQ7u9aRscVl44sLJnokW-sc7ti71EYxdA"
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200: return ""
        soup = BeautifulSoup(res.text, 'html.parser')
        # Ambil teks dari elemen penting saja
        for s in soup(['script', 'style', 'nav', 'footer']): s.decompose()
        text = soup.get_text(" ", strip=True)
        return text[:4000] # Ambil lebih banyak teks
    except:
        return ""

def analyze_scholarship(data_list):
    print("--- AI Sedang Membedah Data... ---")
    combined_data = "\n---\n".join(data_list)
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"DATA INTERNET:\n{combined_data}\n\nTUGAS: Cari beasiswa S1 Computer Science di Taiwan/Malaysia. Fokus ke syarat IELTS 6.0. List Nama Beasiswa, Deadline, dan Link. Jika data tidak lengkap, berikan estimasi berdasarkan info yang ada."
            }]
        }]
    }
    res = requests.post(URL_API, headers={'Content-Type': 'application/json'}, data=json.dumps(prompt))
    return res.json()['candidates'][0]['content']['parts'][0]['text'] if res.status_code == 200 else "API Error"

# --- MAIN PROCESS ---
# Kita pake query yang lebih umum biar dapet banyak hasil
query = "scholarship computer science Taiwan Malaysia S1 2025 2026"
print(f"--- Hunting: {query} ---")

raw_contents = []
with DDGS() as ddgs:
    # Ambil 5 hasil
    results = list(ddgs.text(query, max_results=5))
    
    for i, r in enumerate(results):
        link = r['href']
        print(f"[{i+1}] Mencoba baca: {link}")
        text = get_content(link)
        if text:
            print(f"    (OK) Berhasil ambil {len(text)} karakter.")
            raw_contents.append(f"SUMBER: {link}\nKONTEN: {text}")
        else:
            print(f"    (Gagal) Website ini nolak bot.")
        time.sleep(1)

if raw_contents:
    print("\n" + "="*50 + "\nHASIL TEMUAN AGENT:\n" + "="*50)
    print(analyze_scholarship(raw_contents))
else:
    print("\nNaf, internet lagi pelit data. Coba ganti query lo jadi lebih simpel, misal: 'beasiswa s1 taiwan computer science'")