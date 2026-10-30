import streamlit as st
import requests
import time

st.set_page_config(
    page_title="AI Personal Portfolio Website Builder",
    page_icon="🌐",
    layout="wide"
)

# Tech developer blueprint + dark radial mesh styling
st.markdown("""
<style>
    /* Force main app container styling */
    .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #0b0f19 !important;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.20) 0%, transparent 45%),
            radial-gradient(circle at 85% 25%, rgba(168, 85, 247, 0.20) 0%, transparent 45%),
            radial-gradient(circle at 50% 80%, rgba(14, 165, 233, 0.15) 0%, transparent 55%),
            linear-gradient(rgba(56, 189, 248, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.08) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 100% 100%, 32px 32px, 32px 32px !important;
        color: #e2e8f0 !important;
    }

    /* Force header transparency so the background shows through */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Elevated tech cards for metrics */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
    }

    /* Input text areas and fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
    }

    /* Gradient action buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4) !important;
    }

    /* Tabs styling */
    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.15) !important;
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE INITIALIZATION -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview"
if "sites_built" not in st.session_state:
    st.session_state.sites_built = 0
if "generated_html" not in st.session_state:
    st.session_state.generated_html = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ----------------- GEMINI REST CALL -----------------
def call_gemini(prompt, key):
    candidate_models = [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-2.0-flash"
    ]
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 4096,
            "temperature": 0.7
        }
    }
    
    clean_key = key.strip()
    errors = []
    
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={clean_key}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            if response.status_code == 200:
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    errors.append(f"{model}: Empty response candidates.")
            else:
                errors.append(f"{model} ({response.status_code}): {response.text[:100]}")
        except Exception as req_err:
            errors.append(f"{model} Exception: {str(req_err)}")
            continue
            
    raise Exception(" | ".join(errors))

# ----------------- 1. LOGIN SCREEN -----------------
if not st.session_state.logged_in:
    st.title("🌐 PortfolioForge AI")
    st.caption("AI-POWERED PERSONAL PORTFOLIO WEBSITE GENERATOR")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Sign In")
        login_name = st.text_input("Full Name:", placeholder="e.g., Narasimmavarman E")
        login_email = st.text_input("Academic / College Email:", placeholder="name@domain.edu")
        login_key = st.text_input("Gemini API Key:", type="password", placeholder="Enter key (AIza...)")
        
        if st.button("Enter Portfolio Studio", use_container_width=True):
            if not login_name.strip() or not login_email.strip():
                st.warning("Please provide your name and email to proceed.")
            else:
                st.session_state.logged_in = True
                st.session_state.username = login_name.strip()
                st.session_state.email = login_email.strip()
                if login_key.strip():
                    st.session_state.api_key = login_key.strip()
                st.rerun()

# ----------------- 2. MAIN APPLICATION -----------------
else:
    top_c1, top_c2 = st.columns([3, 1])
    with top_c1:
        st.title("🌐 PortfolioForge AI")
        st.caption(f"Operator: **{st.session_state.username}** ({st.session_state.email}) | Status: Active")
    with top_c2:
        st.metric("Sites Created", st.session_state.sites_built)
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    tabs = st.tabs(["🏠 Overview", "🚀 Generator", "👁️ Live Preview & Code", "💡 Architecture"])

    # TAB 1: OVERVIEW
    with tabs[0]:
        st.subheader("Autonomous Portfolio Builder Engine")
        st.write("Convert raw credentials, projects, and biographical records into a complete, standalone, production-ready portfolio website.")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Generated Sites", st.session_state.sites_built)
        m2.metric("Output Standard", "Single HTML5")
        m3.metric("Style Engine", "Embedded CSS")
        m4.metric("Inference Engine", "Gemini REST")

    # TAB 2: GENERATOR
    with tabs[1]:
        st.subheader("Configure Portfolio Parameters")
        
        saved_key = st.session_state.get("api_key", "")
        api_key_input = st.text_input("Gemini API Key:", value=saved_key, type="password", placeholder="Enter key (AIza...)")
        
        c_left, c_right = st.columns(2)
        with c_left:
            p_name = st.text_input("Full Name:", value="Narasimmavarman E")
            p_title = st.text_input("Professional Title:", value="AI & Data Science Engineer | Full-Stack Developer")
            p_bio = st.text_area(
                "Short Professional Bio:",
                value="Passionate undergraduate engineer specializing in artificial intelligence architectures, machine learning models, and modern web application development.",
                height=110
            )
        with c_right:
            p_skills = st.text_area(
                "Technical Skills (comma-separated):",
                value="Python, Java, Streamlit, FastAPI, TensorFlow, REST APIs, Git, Docker, SQL",
                height=70
            )
            p_projects = st.text_area(
                "Key Projects (Name and short description):",
                value="1. Ecoza - AI Waste Classification System\n2. Anomaly Detection Dashboard for Microelectronics\n3. LLM Comparison & Benchmarking Hub",
                height=110
            )
            p_theme = st.selectbox("Design Theme:", ["Dark Neon Modern", "Minimalist Clean", "Cyberpunk Violet"])

        if st.button("🚀 Generate Full HTML Portfolio", use_container_width=True):
            if not api_key_input.strip():
                st.error("Please enter a valid Gemini API Key.")
            else:
                st.session_state.api_key = api_key_input.strip()
                prompt = f"""
                You are an expert Frontend Web Designer.
                Create a complete, single-file, production-ready responsive HTML/CSS website for a personal portfolio.
                
                Candidate Information:
                - Name: {p_name}
                - Title: {p_title}
                - Bio: {p_bio}
                - Skills: {p_skills}
                - Projects: {p_projects}
                - Design Style: {p_theme}
                
                Requirements:
                - Include full embedded CSS in a <style> block.
                - Make it look premium, modern, responsive, with sleek card layouts, navbar, hero section, skills chips, project cards, and contact footer.
                - Output ONLY valid raw HTML code without markdown code fences, backticks, or extra explanation.
                """
                
                with st.status("Crafting custom portfolio design...", expanded=True) as status:
                    st.write("🎨 Synthesizing structure, typography, and responsive styles...")
                    try:
                        raw_html = call_gemini(prompt, api_key_input)
                        
                        cleaned_html = raw_html.strip()
                        if cleaned_html.startswith("```html"):
                            cleaned_html = cleaned_html[7:]
                        elif cleaned_html.startswith("```"):
                            cleaned_html = cleaned_html[3:]
                        if cleaned_html.endswith("```"):
                            cleaned_html = cleaned_html[:-3]
                        cleaned_html = cleaned_html.strip()
                        
                        st.session_state.generated_html = cleaned_html
                        st.session_state.sites_built += 1
                        status.update(label="✅ Website Generated Successfully!", state="complete", expanded=False)
                        st.success("Portfolio generated! Switch to '👁️ Live Preview & Code' tab to inspect and download.")
                    except Exception as e:
                        status.update(label="❌ Generation Failed", state="error", expanded=False)
                        st.error(f"Details: {e}")

    # TAB 3: LIVE PREVIEW & CODE
    with tabs[2]:
        st.subheader("Website Live Preview & Export")
        if not st.session_state.generated_html:
            st.info("No website generated yet. Go to the '🚀 Generator' tab and click 'Generate Full HTML Portfolio'.")
        else:
            st.download_button(
                label="📥 Download standalone index.html",
                data=st.session_state.generated_html,
                file_name="index.html",
                mime="text/html",
                use_container_width=True
            )
            
            sub1, sub2 = st.tabs(["🖥️ Live Render Preview", "💻 Raw Source Code"])
            with sub1:
                st.components.v1.html(st.session_state.generated_html, height=750, scrolling=True)
            with sub2:
                st.code(st.session_state.generated_html, language="html")

    # TAB 4: ARCHITECTURE
    with tabs[3]:
        st.subheader("Portfolio Builder Engine Architecture")
        c1, c2 = st.columns(2)
        with c1:
            st.write("### 📱 1. Single-Page Embedded Architecture")
            st.write("Consolidates semantic HTML5 and modern CSS styling into a zero-dependency, standalone file deployable instantly on GitHub Pages, Netlify, or Vercel.")
            st.write("### 🎯 2. Structured Prompt Decomposition")
            st.write("Transforms raw textual inputs into structured web sections with appropriate layout hierarchies.")
        with c2:
            st.write("### ⚡ 3. Real-Time Sandboxed Preview")
            st.write("Uses Streamlit component iframes to render live, interactive visual previews immediately without writing to local disk.")
            st.write("### 🛡️ 4. Multi-Model Failover Resilience")
            st.write("Direct REST execution with automated fallback routines across Gemini models prevents workflow stoppage during high traffic.")