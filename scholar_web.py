import streamlit as st
import google.generativeai as genai
import requests
import re
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

# --- 1. CONFIG & UI STYLE ---
st.set_page_config(page_title="Scholar AI v4.0 (FIXED)", layout="wide", page_icon="🎓")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; background: #4CAF50; color: white; border-radius: 5px; }
    .res-box { background: #262730; padding: 20px; border-radius: 10px; border: 1px solid #464b5d; }
</style>
""", unsafe_allow_html=True)

# --- 2. JANTUNG API (ANTI-404) ---
if "API_KEY" not in st.secrets:
    st.error("Woi Naf, API_KEY belum ada di secrets.toml!")
    st.stop()

genai.configure(api_key=st.secrets["API_KEY"])

@st.cache_resource
def get_safe_model():
    """Mencegah error 404 dengan scan model yang tersedia secara dinamis"""
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Urutan prioritas model
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if target in available:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(available[0])
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

model = get_safe_model()

# --- 3. SCRAPER ENGINE ---
def fetch_web_data(query):
    data = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            for r in results:
                try:
                    h = {'User-Agent': 'Mozilla/5.0'}
                    res = requests.get(r['href'], headers=h, timeout=7)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for s in soup(['script', 'style', 'nav', 'footer']): s.decompose()
                    txt = soup.get_text(" ", strip=True)[:2500]
                    if len(txt) > 200: data.append(txt)
                except: continue
    except: pass
    return "\n\n".join(data)

# --- 4. MAIN UI ---
col1, col2 = st.columns([1, 2.5])

with col1:
    st.title("🎓 Scholar AI")
    st.markdown("---")
    with st.expander("👤 Your Profile", expanded=True):
        ielts = st.number_input("IELTS", 0.0, 9.0, 6.0, 0.5)
        gpa = st.text_input("GPA/Nilai", "8.5/10")
    
    st.markdown("---")
    query = st.text_input("🔍 Cari Beasiswa:", placeholder="Contoh: Beasiswa S1 Taiwan")
    btn = st.button("HUNT NOW! 🚀")

with col2:
    if btn:
        if not query:
            st.warning("Isi dulu kolom pencariannya!")
        else:
            with st.status("🧠 Processing Analysis...", expanded=True) as status:
                # Step 1: Search
                status.write("Hunting data from web...")
                context = fetch_web_data(query)
                
                # Step 2: AI Analysis
                status.write("AI is analyzing your chance...")
                prompt = f"""
                Analisis beasiswa untuk user dengan profil: IELTS {ielts}, GPA {gpa}.
                Query: {query}
                Data Web: {context if context else "Gunakan data internalmu."}
                
                TUGAS:
                1. Buat tabel beasiswa yang relevan (Nama, Syarat, Link/Deadline).
                2. Berikan analisis peluang yang jujur dan berdarah-darah.
                3. Berikan 'Confidence Score: [angka]%' di baris paling akhir.
                """
                
                try:
                    response = model.generate_content(prompt)
                    output = response.text
                    
                    # Tampilkan hasil di box yang rapi
                    st.markdown('<div class="res-box">', unsafe_allow_html=True)
                    st.markdown(output)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Step 3: Visualizer (Regex safe)
                    scores = re.findall(r'(\d+)%', output)
                    if scores:
                        val = int(scores[-1])
                        st.write(f"**Reliabilitas Analisis:** {val}%")
                        st.progress(val / 100.0)
                    
                    status.update(label="Analysis Finished!", state="complete")
                except Exception as e:
                    st.error(f"AI Gagal: {e}")
    else:
        st.info("Input profil lo di sebelah kiri, terus klik Hunt Now!")