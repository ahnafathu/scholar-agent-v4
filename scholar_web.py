import streamlit as st
import requests
import json
import time
import re
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import os

# --- CONFIG & STYLES (MUST BE FIRST) ---
st.set_page_config(page_title="Scholar AI v4.0", page_icon="🎓", layout="wide")

# --- API SETUP ---
API_KEY = st.secrets.get("API_KEY", "KODE_TIDAK_DITEMUKAN")
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200: return ""
        soup = BeautifulSoup(res.text, 'html.parser')
        for s in soup(['script', 'style', 'nav', 'footer', 'header']): s.decompose()
        return soup.get_text(" ", strip=True)[:4000]
    except:
        return ""

# --- SIDEBAR: USER PROFILE ---
st.sidebar.header("👤 Your Profile")
user_ielts = st.sidebar.number_input("Current IELTS Score", 0.0, 9.0, 6.0, 0.5)
user_gpa = st.sidebar.text_input("Your GPA (e.g. 3.8/4.0)", "8.5/10")
st.sidebar.info("This profile helps the AI provide a personalized 'Chance Analysis'.")

# --- MAIN UI ---
st.title("🎓 AI Smart Web Scraper & Scholar Analyst")
st.write("System Status: Online & Ready to Hunt!")
st.markdown("---")

user_input = st.text_input("🔍 Search Query", placeholder="e.g. fully funded computer science scholarship taiwan 2026")

if st.button("HUNT NOW! 🚀"):
    if not user_input:
        st.warning("Please enter your request first, Naf!")
    else:
        # Start the Hunting Process
        with st.status("🔍 Initializing global search...", expanded=True) as status:
            raw_contents = []
            try:
                with DDGS() as ddgs:
                    status.write(f"Searching for: {user_input}")
                    results = list(ddgs.text(user_input, max_results=5))
                
                if not results:
                    status.update(label="No results found.", state="error", expanded=True)
                    st.error(f"Sorry, we couldn't find any data for '{user_input}'. Try changing your keywords.")
                else:
                    status.update(label="Sources found! Extracting data...", state="running")
                    
                    for i, r in enumerate(results):
                        link = r['href']
                        status.write(f"Reading Source {i+1}: {link}")
                        content = get_content(link)
                        if content:
                            raw_contents.append(f"SOURCE {i+1}: {link}\nDATA: {content}")
                        time.sleep(1) # Anti-block delay

                    if not raw_contents:
                        status.update(label="Extraction failed.", state="error")
                        st.error("Found links, but couldn't read the content. The websites might be blocking access.")
                    else:
                        status.update(label="Data extracted. Generating Strategic Report...", state="running")
                        
                        # --- AI ANALYSIS BLOCK ---
                        prompt_text = f"""
                        CONTEXT DATA: {" ".join(raw_contents)}
                        USER REQUEST: {user_input}
                        USER PROFILE: IELTS {user_ielts}, GPA {user_gpa}
                        
                        TASK: Generate a professional and comprehensive report in English.
                        1. SCHOLARSHIP TABLE: (Name, Provider, Country, Deadline, Requirements, Link).
                        2. ELIGIBILITY MATCH: Compare user's IELTS/GPA with the scholarship requirements found.
                        3. BRUTALLY HONEST ADVICE: Is the user a strong candidate? What are the missing links? Should they apply or improve scores first?
                        4. STRATEGIC STEPS: Next 3 actions the user must take.
                        """
                        
                        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
                        res = requests.post(URL_API, json=payload)
                        
                        if res.status_code == 200:
                            status.update(label="Analysis complete!", state="complete", expanded=False)
                            laporan = res.json()['candidates'][0]['content']['parts'][0]['text']
                            
                            st.subheader("📊 Strategic Analysis Report")
                            st.markdown(laporan)
                            
                            # DOWNLOAD BUTTON
                            st.download_button(
                                label="📥 Download Report (.md)",
                                data=laporan,
                                file_name=f"Scholar_Report_{user_input.replace(' ', '_')}.md",
                                mime="text/markdown"
                            )
                        else:
                            status.update(label="AI Brain Error.", state="error")
                            st.error(f"API Error (Status: {res.status_code}). Please check your Gemini API Key in Secrets.")
            
            except Exception as e:
                status.update(label="System Error.", state="error")
                st.error(f"An unexpected error occurred: {str(e)}")

st.markdown("---")
st.caption("Engineered by Ahnaf | AI Scholar Analyst v4.0")