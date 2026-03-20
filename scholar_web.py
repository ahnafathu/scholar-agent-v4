import streamlit as st
import requests
import json
import time
import re
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import os

# --- 1. CONFIG & STYLES (MUST BE FIRST) ---
st.set_page_config(page_title="Scholar AI v4.0", page_icon="🎓", layout="wide")

# --- 2. API SETUP ---
# Mengambil API Key dari Secrets Streamlit untuk keamanan
API_KEY = st.secrets.get("API_KEY", "KODE_TIDAK_DITEMUKAN")
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200: return ""
        soup = BeautifulSoup(res.text, 'html.parser')
        # Membersihkan elemen sampah agar token AI hemat
        for s in soup(['script', 'style', 'nav', 'footer', 'header']): s.decompose()
        return soup.get_text(" ", strip=True)[:4000]
    except:
        return ""

# --- 3. SIDEBAR: USER PROFILE ---
st.sidebar.header("👤 Your Profile")
user_ielts = st.sidebar.number_input("Current IELTS Score", 0.0, 9.0, 6.0, 0.5)
user_gpa = st.sidebar.text_input("Your GPA (e.g. 3.8/4.0)", "8.5/10")
st.sidebar.info("This profile helps the AI provide a personalized 'Chance Analysis'.")

# --- 4. MAIN UI ---
st.title("🎓 AI Smart Web Scraper & Scholar Analyst")
st.write("System Status: Online & Ready to Hunt!")
st.markdown("---")

user_input = st.text_input("🔍 Search Query", placeholder="Tulis apa saja, misal: beasiswa full funded S1 di Taiwan")

if st.button("HUNT NOW! 🚀"):
    if not user_input:
        st.warning("Please enter your request first, Naf!")
    else:
        with st.status("🧠 AI is thinking & searching...", expanded=True) as status:
            # STEP A: SMART QUERY EXPANSION
            # AI bakal bikin keyword tambahan secara otomatis biar pencarian lebih luas
            search_queries = [user_input]
            try:
                refine_payload = {
                    "contents": [{"parts": [{"text": f"Ganti input ini: '{user_input}' menjadi 2 keyword pencarian beasiswa dalam bahasa Inggris yang paling efektif. Pisahkan dengan koma saja tanpa penjelasan lain."}]}]
                }
                refine_res = requests.post(URL_API, json=refine_payload)
                if refine_res.status_code == 200:
                    suggestions = refine_res.json()['candidates'][0]['content']['parts'][0]['text']
                    search_queries.extend([s.strip() for s in suggestions.split(",")])
            except: 
                pass

            # STEP B: MULTI-KEYWORD SEARCHING
            raw_contents = []
            with DDGS() as ddgs:
                # Coba maksimal 2 query terbaik untuk efisiensi
                for q in search_queries[:2]:
                    status.write(f"Searching for: {q}...")
                    try:
                        results = list(ddgs.text(q, max_results=3))
                        for r in results:
                            link = r['href']
                            status.write(f"Reading: {link}")
                            content = get_content(link)
                            if content:
                                raw_contents.append(f"SOURCE: {link}\nDATA: {content}")
                            time.sleep(1) # Delay anti-block
                    except:
                        continue
            
            # STEP C: FINAL ANALYSIS
            if not raw_contents:
                status.update(label="No data found.", state="error")
                st.error("I couldn't find enough information. Please try a more general topic.")
            else:
                status.update(label="Analyzing data & generating report...", state="running")
                
                # Prompt instruksi agar AI fleksibel secara bahasa dan jujur
                prompt_text = f"""
                You are a world-class Scholarship Consultant.
                DATA FOUND: {" ".join(raw_contents)}
                USER REQUEST: {user_input}
                USER PROFILE: IELTS {user_ielts}, GPA {user_gpa}
                
                STRICT RULES:
                1. LANGUAGE: Respond using the SAME LANGUAGE used in the 'USER REQUEST'.
                2. STRUCTURE: 
                   - Scholarship Table (Name, Provider, Deadline, Link).
                   - Eligibility Match: Comparison between user profile and requirements.
                   - Brutally Honest Advice: Direct feedback on the user's chances.
                   - Strategic Next Steps: 3 clear actions to take.
                3. HONESTY: Do not sugarcoat. If the user's score is too low, say it clearly.
                """
                
                payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
                res = requests.post(URL_API, json=payload)
                
                if res.status_code == 200:
                    status.update(label="Analysis complete!", state="complete", expanded=False)
                    laporan = res.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    st.subheader("📊 Strategic Analysis Report")
                    st.markdown(laporan)
                    
                    st.download_button(
                        label="📥 Download Report (.md)",
                        data=laporan,
                        file_name=f"Scholar_Report_{int(time.time())}.md",
                        mime="text/markdown"
                    )
                else:
                    status.update(label="AI Analysis failed.", state="error")
                    st.error("The AI encountered an error. Check your API Key in Streamlit Secrets.")

st.markdown("---")
st.caption("Engineered by Ahnaf | Scholar AI v4.0 | No Fluff, Just Truth.")