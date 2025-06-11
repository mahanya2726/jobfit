# JobFit – Smart ATS Resume Analyzer

Optimize your resume using AI and beat the bots!

JobFit is a powerful web app that analyzes your resume against any job description using Google Gemini AI. It helps job seekers optimize their resumes to pass through Applicant Tracking Systems (ATS) with higher success rates.

🔍 It summarizes your resume, gives improvement suggestions, recommends courses, and gives a visual ATS match score — all in one click.

## 🚀 Features

- 📄 Upload PDF resumes
- ✨ Uses Google Gemini AI for analysis
- 📋 Resume summary generation
- 📈 Skill improvement suggestions with course links
- 🎯 ATS Match Score visualization
- 🖥️ Clean, interactive Streamlit interface

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Generative AI (Gemini)
- pdf2image, Pillow
- Plotly
- dotenv, requests

## ⚙️ Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/mahanya2726/jobfit.git
   cd jobfit

2. **Create Virtual Environment**
    ```bash
    python -m venv myenv
    myenv\Scripts\activate  # On Windows
    source myenv/bin/activate  # On macOS/Linux
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Add your Gemini API key**
    Create a .env file in the root folder.
    ```bash
    GOOGLE_API_KEY=your_api_key_here
    ```

5. **Run the app**
    ```bash
    streamlit run app.py
    ```

