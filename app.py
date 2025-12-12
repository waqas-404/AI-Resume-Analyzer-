import streamlit as st
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Download NLTK resources
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #0f1419 100%);
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 0 30px 0;
        margin-bottom: 20px;
    }
    
    .logo-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    .logo-text {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 32px;
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
        line-height: 1.3;
    }
    
    .hero-subtitle {
        font-size: 16px;
        color: #a0aec0;
        line-height: 1.6;
    }
    
    /* Card styling */
    .custom-card {
        background: rgba(26, 35, 50, 0.6);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .card-icon {
        font-size: 24px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a2332 0%, #0f1419 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 16px;
        padding: 12px 32px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 16px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(26, 35, 50, 0.4);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 20px;
    }
    
    .stFileUploader label {
        color:rgb(36, 30, 30) !important;
        font-weight: 600;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: rgba(26, 35, 50, 0.6) !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 14px !important;
    }
    
    .stTextArea label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* Metric styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 20px;
    }
    
    div[data-testid="stMetric"] label {
        color: #a0aec0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 42px !important;
        font-weight: 800 !important;
    }
    
    /* Alert styling */
    .stAlert {
        background: rgba(26, 35, 50, 0.8) !important;
        border-radius: 12px !important;
        border-left: 4px solid !important;
    }
    
    /* Info box */
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        color: #e2e8f0;
    }
    
    .info-box-title {
        font-weight: 700;
        color: #667eea;
        margin-bottom: 8px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Results section */
    .result-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        margin-top: 16px;
    }
    
    .badge-low {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    
    .badge-good {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
        border: 1px solid #fbbf24;
    }
    
    .badge-excellent {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="logo-container">
    <div class="logo-icon">🤖</div>
    <div class="logo-text">AI Resume Analyzer</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <div class="hero-title">Smart Resume Matching with AI-Powered Analysis</div>
    <div class="hero-subtitle">
        Upload your resume and job description to get instant insights on how well they match. 
        Our advanced AI uses TF-IDF and Cosine Similarity algorithms to provide accurate compatibility scores.
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="card-title"><span class="card-icon">ℹ️</span> About This Tool</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <div class="info-box-title">What You Get:</div>
        ✓ Instant compatibility score<br>
        ✓ Job keyword analysis<br>
        ✓ Resume optimization tips<br>
        ✓ AI-powered recommendations
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="card-title" style="margin-top: 32px;"><span class="card-icon">🔄</span> How It Works</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <strong>1.</strong> Upload your resume (PDF format)<br><br>
        <strong>2.</strong> Paste the job description<br><br>
        <strong>3.</strong> Click "Analyze Match"<br><br>
        <strong>4.</strong> Review your compatibility score and insights
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="card-title" style="margin-top: 32px;"><span class="card-icon">⚙️</span> Technology</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Built with:<br>
        • TF-IDF Vectorization<br>
        • Cosine Similarity<br>
        • Natural Language Processing<br>
        • Machine Learning
    </div>
    """, unsafe_allow_html=True)

# Helper functions (unchanged)
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text = text + page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return " ".join([word for word in words if word not in stop_words])

def calculate_similarity(resume_text, job_description):
    resume_processed = remove_stopwords(clean_text(resume_text))
    job_processed = remove_stopwords(clean_text(job_description))
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_processed, job_processed])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    return round(score, 2), resume_processed, job_processed


# def extract_keywords(text,num_keywords=10): 
    # words=word_tokenize(text) 
    # words=[w for w in words if len(w)>2] 
    # tagged_words=pos_tag(words) 
    # nouns=[w for w,pos in tagged_words if pos.startswith('NN') or pos.startswith('JJ')] 
    # word_freq=Counter(nouns) # return word_freq.most_common(num_keywords)


def main():
    # Input section with cards
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="card-icon">📄</span> Upload Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose your resume PDF file", type=['pdf'], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span class="card-icon">💼</span> Job Description</div>', unsafe_allow_html=True)
        job_description = st.text_area("Paste the job description here", height=200, label_visibility="collapsed", placeholder="Paste the complete job description here...")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Analyze Match", use_container_width=True):
        if not uploaded_file:
            st.warning("⚠️ Please upload your resume to continue")
            return
        if not job_description:
            st.warning("⚠️ Please paste the job description to continue")
            return
        
        with st.spinner("🔍 Analyzing your resume with AI..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not resume_text:
                st.error("❌ Could not extract text from PDF. Please try another file.")
                return
            
            # Calculate similarity
            similarity_score, resume_processed, job_processed = calculate_similarity(resume_text, job_description)
            
            st.markdown("---")
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title"><span class="card-icon">📊</span> Analysis Results</div>', unsafe_allow_html=True)
            
            # Score display
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.metric("Match Score", f"{similarity_score:.1f}%")
            
            fig, ax = plt.subplots(figsize=(10, 1.5))
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            # Create gradient effect with multiple segments
            segments = [(0, 40, '#ef4444'), (40, 70, '#fbbf24'), (70, 100, '#10b981')]
            for start, end, color in segments:
                ax.barh([0], [end - start], left=[start], color=color, alpha=0.3, height=0.6)
            
            # Score bar
            if similarity_score <= 40:
                color = '#ef4444'
            elif similarity_score <= 70:
                color = '#fbbf24'
            else:
                color = '#10b981'
            
            ax.barh([0], [similarity_score], color=color, height=0.6, 
                   edgecolor='white', linewidth=2, alpha=0.9)
            
            # Styling
            ax.set_xlim(0, 100)
            ax.set_ylim(-0.5, 0.5)
            ax.set_xlabel("Match Percentage", fontsize=12, color='white', fontweight='600')
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_color('#667eea')
            ax.tick_params(axis='x', colors='white', labelsize=10)
            ax.grid(axis='x', alpha=0.2, linestyle='--', color='white')
            
            # Add percentage markers
            for i in [0, 25, 50, 75, 100]:
                ax.text(i, -0.35, f'{i}%', ha='center', va='top', 
                       color='#a0aec0', fontsize=9, fontweight='600')
            
            st.pyplot(fig, use_container_width=True)
            plt.close()
            
            st.markdown("<br>", unsafe_allow_html=True)
            if similarity_score < 40:
                st.markdown('<div class="result-badge badge-low">🔴 Low Match - Needs Improvement</div>', unsafe_allow_html=True)
                st.warning("""
                **Recommendation:** Your resume needs significant tailoring to match this job description. 
                Consider incorporating more relevant keywords and highlighting applicable experiences.
                """)
            elif similarity_score < 70:
                st.markdown('<div class="result-badge badge-good">🟡 Good Match - Room for Improvement</div>', unsafe_allow_html=True)
                st.info("""
                **Recommendation:** Your resume aligns fairly well with the job requirements. 
                Fine-tune your resume by emphasizing key skills mentioned in the job description.
                """)
            else:
                st.markdown('<div class="result-badge badge-excellent">🟢 Excellent Match - Well Aligned</div>', unsafe_allow_html=True)
                st.success("""
                **Recommendation:** Outstanding! Your resume strongly aligns with the job description. 
                You have a great foundation - ensure your cover letter also highlights these matching points.
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
