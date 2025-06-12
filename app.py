from dotenv import load_dotenv
import io
import base64
import os
import requests
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
import re
import json

# --- Load environment variables ---
load_dotenv()

# --- Configure Gemini API ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Graph ---
def show_match_score_donut(score):
    fig = go.Figure(data=[go.Pie(
        labels=["Match", "Gap"],
        values=[score, 100 - score],
        hole=0.6,
        marker_colors=["#00CC96", "#FF6361"],
        textinfo='none'
    )])

    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[dict(text=f"{score}%", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    return fig

# --- Lottie animation loader ---
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

lottieresume=load_lottiefile("resumeanimation.json")

# --- Gemini content generator ---
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    full_prompt = f"Job Description:\n{input_text}\n\nInstruction:\n{prompt}"
    response = model.generate_content([full_prompt, pdf_content[0]])
    return response.text



# --- PDF file processing ---
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="JobFit", page_icon="📄", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        .stTextArea textarea {
            height: 180px !important;
        }
        .img-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            margin-top: -30px;
        }
        div.stButton > button:first-child {
            font-size: 18px;
            font-weight: 600;
            background-color: #007bff;  /* Blue */
            color: white;
            padding: 0.5em 1.5em;
            border: none;
            border-radius: 8px;
            cursor: pointer; 
        }
        div.stButton > button:first-child:hover {
            background-color: #0056b3;  /* Darker blue */
            transform: scale(1.03);
        }
        div.stButton > button:first-child:focus {
            outline: none !important;
            box-shadow: none !important;
            color: white !important;               /* Keep white after click */
        }
        
    </style>
""", unsafe_allow_html=True)

# --- Title Section ---
st.markdown("<h1 style='text-align: center; color: #FF8C00;'>JobFit</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; font-size:20px; font-weight:1000; margin-bottom:1px;'>Smart ATS Resume Analyzer</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Layout Columns ---
col0, col1, col2 = st.columns([0.2, 1, 2])

# --- LEFT COLUMN: Description and Image ---
with col1:
    st_lottie(
        lottieresume,
        speed=60,
        reverse=False,
        loop=True,
        quality="low",
        height=None,
        width=None,
        key=None,

    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT COLUMN: Upload & Input ---
with col2:
    st.markdown("<div style='font-size:20px; font-weight:1000; margin-bottom:1px;'>📎 Upload Your Resume (PDF)</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(label="", type=["pdf"])

    st.markdown("<div style='font-size:20px; font-weight:1000; margin-top:15px; margin-bottom:1px;'>📝 Paste Job Description</div>", unsafe_allow_html=True)
    input_text = st.text_area(label="", height=180)

    # ---- Prompts ----
    prompt1 = "You are an expert resume reviewer. Analyze this resume and provide a clear, concise summary..."
    prompt2 = (
        "You are a professional career coach and resume reviewer. Analyze this resume based on the job description. "
        "Identify specific areas where the candidate can improve to be a stronger fit for the job. "
        "For each improvement point:\n"
        "- Clearly state the issue.\n"
        "- Provide a practical suggestion.\n"
        "- If possible, recommend an **online course** with a direct link to help upskill in that area (prefer Coursera, Udemy, freeCodeCamp).\n\n"
        "Format your response like this:\n\n"
        "### Area for Improvement: <Title>\n"
        "- **Issue:** <What’s missing or weak>\n"
        "- **Suggestion:** <How to fix it>\n"
        "- **Course Recommendation (if applicable):** [Course Title](Course Link)\n"
    )

    prompt3 = (
        "You are an ATS system. Based on the job description and resume, evaluate the match percentage "
        "for the candidate and respond with:\n"
        "Match Score: X%\n"
        "Also briefly explain why you gave this score, mentioning relevant strengths and missing points.\n"
        "Make sure the score is the first line and clearly written as: Match Score: 85%."
    )

    def extract_score_from_text(response_text):
        match = re.search(r"Match Score:\s*(\d+)%", response_text)
        return int(match.group(1)) if match else None

    if st.button("🔍 Scan Resume"):
        if uploaded_file and input_text:
            pdf_content = input_pdf_setup(uploaded_file)
            st.success("✅ Resume scanned successfully! Choose what you'd like to analyze below.")

            tab1, tab2, tab3 = st.tabs(["📋 Summary", "📈 Improve Skills", "🎯 Match Score"])

            with tab1:
                with st.spinner("Generating summary..."):
                    summary_response = get_gemini_response(input_text, pdf_content, prompt1)
                    st.subheader("📋 Resume Summary")
                    st.write(summary_response)

            with tab2:
                with st.spinner("Identifying skill improvements..."):
                    improvement_response = get_gemini_response(input_text, pdf_content, prompt2)
                    st.subheader("📈 Skill Improvement Suggestions")
                    st.write(improvement_response)

            with tab3:
                with st.spinner("Evaluating match percentage..."):
                    match_response = get_gemini_response(input_text, pdf_content, prompt3)
                    
                   

                    match_score = extract_score_from_text(match_response)
                    if match_score is not None:
                        st.markdown("### 🎯 ATS Match Score")
                        st.plotly_chart(show_match_score_donut(match_score), use_container_width=True)
                    else:
                        st.warning("❌ Couldn't extract a match score from the response.")
                    st.subheader("🎯 ATS Match Report")
                    st.write(match_response)
        else:
            st.warning("⚠️ Please upload your resume and paste the job description.")

