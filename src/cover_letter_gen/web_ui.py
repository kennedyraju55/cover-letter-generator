"""Streamlit Web UI for Cover Letter Generator."""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from cover_letter_gen.core import (
    generate_cover_letter,
    load_config,
    get_tones,
    match_skills,
    save_revision,
    list_revisions,
    TONES,
)

# Custom CSS for professional dark theme
st.set_page_config(page_title="Cover Letter Generator", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { background: linear-gradient(180deg, #0e1117 0%, #1a1a2e 100%); }
    h1 { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem !important; }
    h2 { color: #667eea !important; }
    h3 { color: #a78bfa !important; }
    .stButton>button { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; padding: 0.5rem 2rem; font-weight: 600; transition: transform 0.2s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #1a1a2e; border: 1px solid #333; color: #e0e0e0; border-radius: 8px; }
    .stSelectbox>div>div { background-color: #1a1a2e; border: 1px solid #333; }
    .stMetric { background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 1rem; border-radius: 10px; border: 1px solid #333; }
    .css-1d391kg { background-color: #1a1a2e; }
    div[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); }
    .stSuccess { background-color: rgba(102, 126, 234, 0.1); border: 1px solid #667eea; }
    footer { visibility: hidden; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("✉️ Cover Letter Generator")
    st.markdown("*Generate personalized, AI-powered cover letters that get interviews*")

    config = load_config("config.yaml")
    tones = get_tones()

    tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume & JD Upload", "✉️ Generated Letter", "🎯 Skill Match", "📝 Revision History"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📄 Resume")
            resume_text = st.text_area("Paste your resume", height=250, placeholder="Paste your resume text here...")
            resume_file = st.file_uploader("Or upload resume", type=["txt", "md"], key="resume_upload")
            if resume_file:
                resume_text = resume_file.read().decode("utf-8")
                st.success(f"Loaded {len(resume_text)} chars")

        with col2:
            st.subheader("📋 Job Description")
            jd_text = st.text_area("Paste job description", height=250, placeholder="Paste the job description here...")
            jd_file = st.file_uploader("Or upload JD", type=["txt", "md"], key="jd_upload")
            if jd_file:
                jd_text = jd_file.read().decode("utf-8")
                st.success(f"Loaded {len(jd_text)} chars")

        col1, col2, col3 = st.columns(3)
        with col1:
            company = st.text_input("Company Name", placeholder="e.g., Google")
        with col2:
            tone_key = st.selectbox("Tone", list(tones.keys()),
                                     format_func=lambda x: f"{tones[x]['icon']} {tones[x]['name']}")
        with col3:
            name = st.text_input("Your Name (optional)", placeholder="e.g., Jane Doe")

        if st.button("🚀 Generate Cover Letter", type="primary", use_container_width=True):
            if not resume_text or not jd_text or not company:
                st.error("Please provide resume, job description, and company name.")
            else:
                skill_match = match_skills(resume_text, jd_text)
                st.session_state["skill_match"] = skill_match

                with st.spinner("Writing your cover letter..."):
                    try:
                        result = generate_cover_letter(
                            resume_text, jd_text, company, tone_key, name or None, skill_match, config
                        )
                        st.session_state["cover_letter"] = result
                        st.session_state["cl_company"] = company
                        st.session_state.setdefault("revision_count", 0)
                        st.session_state["revision_count"] += 1
                        save_revision(result, company, st.session_state["revision_count"], config)
                        st.success("Cover letter generated!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab2:
        if "cover_letter" in st.session_state:
            st.subheader(f"✉️ Cover Letter for {st.session_state.get('cl_company', 'Company')}")
            st.markdown(st.session_state["cover_letter"])

            word_count = len(st.session_state["cover_letter"].split())
            st.caption(f"Word count: ~{word_count}")

            st.download_button("📄 Download Cover Letter",
                                st.session_state["cover_letter"],
                                file_name="cover_letter.md",
                                mime="text/markdown")
        else:
            st.info("Generate a cover letter first.")

    with tab3:
        if "skill_match" in st.session_state:
            sm = st.session_state["skill_match"]

            st.metric("Overall Skill Match", f"{sm['match_percentage']}%")

            for cat in ["technical", "soft", "domain"]:
                st.markdown(f"### {cat.title()} Skills")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**✅ Matched:**")
                    for s in sm["matched"][cat]:
                        st.markdown(f"- {s}")
                    if not sm["matched"][cat]:
                        st.markdown("*None*")
                with col2:
                    st.markdown("**❌ Missing:**")
                    for s in sm["missing"][cat]:
                        st.markdown(f"- {s}")
                    if not sm["missing"][cat]:
                        st.markdown("*None*")
                with col3:
                    st.markdown("**💡 Extra:**")
                    for s in sm["extra"][cat]:
                        st.markdown(f"- {s}")
                    if not sm["extra"][cat]:
                        st.markdown("*None*")
        else:
            st.info("Generate a cover letter to see skill analysis.")

    with tab4:
        st.subheader("📝 Revision History")
        revs = list_revisions(config=config)
        if revs:
            for r in revs:
                st.text(f"  {r['filename']}  ({r['size']:,} B)  {r['modified'][:19]}")
        else:
            st.info("No revisions saved yet.")


if __name__ == "__main__":
    main()
