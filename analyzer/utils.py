import PyPDF2
import re
from collections import Counter
import nltk
nltk.data.path.append("/usr/local/nltk_data")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources (do this once)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger_eng')

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

def clean_text(text):
    """Clean and normalize text"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def remove_stopwords(text):
    """Remove common stopwords from text"""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return " ".join([word for word in words if word not in stop_words])

def calculate_similarity(resume_text, job_description):
    """Calculate cosine similarity between resume and job description"""
    resume_processed = remove_stopwords(clean_text(resume_text))
    job_processed = remove_stopwords(clean_text(job_description))
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_processed, job_processed])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    
    return round(score, 2), resume_processed, job_processed

def extract_keywords(text, num_keywords=10):
    """Extract important keywords from text using POS tagging"""
    words = word_tokenize(text.lower())
    words = [w for w in words if len(w) > 2]
    tagged_words = pos_tag(words)
    
    # Keep nouns, adjectives, and verbs
    keywords = [w for w, pos in tagged_words 
                if pos.startswith('NN') or pos.startswith('JJ') or pos.startswith('VB')]
    
    word_freq = Counter(keywords)
    top_keywords = [word for word, freq in word_freq.most_common(num_keywords)]
    return top_keywords

def find_missing_keywords(resume_text, job_description, num_keywords=10):
    """Find keywords present in job description but missing in resume"""
    job_keywords = extract_keywords(job_description, num_keywords)
    resume_keywords = extract_keywords(resume_text, num_keywords * 2)
    
    missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
    matching_keywords = [kw for kw in job_keywords if kw in resume_keywords]
    
    return job_keywords, matching_keywords, missing_keywords