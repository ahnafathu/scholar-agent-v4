import streamlit as st
import requests
import json
import time
import re
from ddgs import DDGS
from bs4 import BeautifulSoup

# --- CONFIG & STYLES ---
st.set_page_config(page_title="Scholar AI v4.0", page_icon="🎓", layout="wide")
API_KEY = "AIzaSyCQ7u9aRscVl44sLJnokW-sc7ti71EYxdA"
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200: return ""
        soup = BeautifulSoup(res.text, 'html.parser')
        for s in soup(['script', 'style', 'nav', 'footer', 'header']): s.decompose()
        return soup.get_text(" ", strip=True)[:4000]
    except: return ""

# --- SIDEBAR: USER PROFILE ---
st.sidebar.header("👤 Your Profile (Advanced Matching)")
user_ielts = st.sidebar.number_input("Current IELTS Score", 0.0, 9.0, 6.0, 0.5)
user_gpa = st.sidebar.text_input("Your GPA (e.g. 3.8/4.0)", "8.5/10")
st.sidebar.info("Profile ini bakal dipake AI buat ngasih 'Analisis Peluang' yang lebih personal.")

# --- MAIN UI ---
st.title("🎓 AI Smart Web Scraper & Scholar Analyst")
st.markdown("---")

user_input = st.text_input("🔍 Tanya apa saja...", placeholder="Contoh: beasiswa s1 computer science taiwan full funded")

if st.button("HUNT NOW! 🚀"):
    if not user_input:
        st.warning("Isi dulu request-nya, Naf!")
    else:
        with st.status("Searching the web...", expanded=True) as status:
            raw_contents = []
            with DDGS() as ddgs:
                results = list(ddgs.text(user_input, max_results=5))
                for i, r in enumerate(results):
                    link = r['href']
                    st.write(f"Scanning: {link}")
                    content = get_content(link)
                    if content:
                        raw_contents.append(f"SUMBER {i+1}: {link}\nDATA: {content}")
                    time.sleep(1)
            status.update(label="Analysis complete!", state="complete", expanded=False)

        if raw_contents:
            st.subheader("📊 Strategic Analysis Report")
            
            # PROMPT DENGAN KONTEKS PROFIL USER
            prompt_text = f"""
            DATA: {" ".join(raw_contents)}
            REQUEST: {user_input}
            USER_PROFILE: IELTS {user_ielts}, GPA {user_gpa}
            
            TUGAS: Buat laporan sangat rapi. 
            1. Tabel Beasiswa (Nama, Negara, Deadline, Link).
            2. Analisis Kecocokan: Bandingkan profil user (IELTS/GPA) dengan syarat beasiswa tersebut.
            3. Berikan 'Brutally Honest Advice' apakah user layak apply atau harus upgrade skor dulu.
            """
            
            payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
            res = requests.post(URL_API, json=payload)
            
            if res.status_code == 200:
                laporan = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.markdown(laporan)
                
                # DOWNLOAD BUTTON
                st.download_button(
                    label="📥 Download Report (.md)",
                    data=laporan,
                    file_name=f"Scholar_Report_{user_input.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            else:
                st.error("AI Brain Error. Cek API Key lo.")