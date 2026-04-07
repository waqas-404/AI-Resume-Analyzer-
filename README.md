# 🤖 AI Resume Analyzer

A powerful Django-based web application that uses AI and Machine Learning to analyze resumes against job descriptions, providing instant compatibility scores and actionable insights.

🔗 **Live Demo:** [ai-resume-analyzer-jbuu.onrender.com](https://ai-resume-analyzer-jbuu.onrender.com)

<img width="930" height="607" alt="image" src="https://github.com/user-attachments/assets/48c59584-b949-4eb5-8ad1-54fcbca14d18" />


## ✨ Features

- **Smart Resume Matching**: Upload your resume (PDF) and paste a job description to get an instant compatibility score
- **AI-Powered Analysis**: Uses TF-IDF Vectorization and Cosine Similarity algorithms for accurate matching
- **Keyword Extraction**: Identifies key skills and keywords from job descriptions
- **Gap Analysis**: Highlights missing keywords that you should include in your resume
- **Visual Results**: Interactive score visualization with color-coded match levels (Low, Good, Excellent)
- **Analysis History**: Track all your past resume analyses
- **CRUD Operations**: View, analyze, and delete analysis records
- **Responsive Design**: Modern, gradient-based UI with smooth animations
- **Database Persistence**: All analyses are saved to the database for future reference
- **User Authentication**: Secure user registration and login system

## 🛠️ Technology Stack

### Backend
- **Django 4.x**: Web framework
- **Python 3.8+**: Programming language
- **SQLite**: Default database (easily switchable to PostgreSQL/MySQL)

### Machine Learning & NLP
- **scikit-learn**: TF-IDF Vectorization and Cosine Similarity
- **NLTK**: Natural Language Processing
  - Tokenization
  - Stopwords removal
  - POS (Part-of-Speech) tagging

### PDF Processing
- **PyPDF2**: PDF text extraction

### Frontend
- **HTML5 & CSS3**: Modern, gradient-based UI
- **JavaScript**: Interactive elements

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```bash
python -m nltk.downloader punkt stopwords averaged_perceptron_tagger
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📦 Requirements

Create a `requirements.txt` file with:

```txt
Django>=4.0,<5.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
PyPDF2>=3.0.0
nltk>=3.8.0
pillow>=9.0.0
```

## 🎯 Usage

### 1. Upload Resume
- Navigate to the home page
- Click on "Upload Resume" and select your PDF resume
- The application supports PDF format only

### 2. Paste Job Description
- Copy the complete job description from the job posting
- Paste it into the "Job Description" text area

### 3. Analyze Match
- Click the "🚀 Analyze Match" button
- Wait for the AI to process your resume

### 4. View Results
- **Match Score**: See your compatibility percentage (0-100%)
- **Color-Coded Rating**:
  - 🔴 Red (0-40%): Low Match - Needs Improvement
  - 🟡 Yellow (40-70%): Good Match - Room for Improvement
  - 🟢 Green (70-100%): Excellent Match - Well Aligned
- **Keyword Analysis**: View matching and missing keywords
- **Recommendations**: Get actionable advice to improve your resume

### 5. View History
- Access your analysis history from the History page
- View details of past analyses
- Delete unwanted records

## 📁 Project Structure

```
ai-resume-analyzer/
├── manage.py
├── requirements.txt
├── README.md
├── resume_analyzer_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── analyzer/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── utils.py
│   ├── templates/
│   │   └── analyzer/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── results.html
│   │       └── history.html
│   └── migrations/
└── media/
    └── resumes/
```

## 🧠 How It Works

### 1. Text Extraction
```python
PyPDF2 extracts text from uploaded PDF resumes
```

### 2. Text Preprocessing
```python
- Convert to lowercase
- Remove special characters
- Tokenization
- Remove stopwords (common words like "the", "is", "and")
```

### 3. TF-IDF Vectorization
```python
- Converts text into numerical vectors
- TF (Term Frequency): How often a word appears
- IDF (Inverse Document Frequency): Importance of the word
```

### 4. Cosine Similarity
```python
- Measures the angle between two vectors
- Score ranges from 0 (no similarity) to 1 (identical)
- Multiplied by 100 to get percentage
```

### 5. Keyword Extraction
```python
- Uses POS tagging to identify nouns, verbs, and adjectives
- Extracts most frequent important words
- Compares job keywords with resume keywords
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with upload form |
| POST | `/` | Submit resume and job description for analysis |
| GET | `/results/<int:pk>/` | View analysis results |
| GET | `/history/` | View all past analyses |
| POST | `/delete/<int:pk>/` | Delete a specific analysis |
| GET | `/admin/` | Django admin panel |

## 🚀 Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn resume_analyzer_project.wsgi
```

3. Create `runtime.txt`:
```
python-3.10.12
```

4. Update `requirements.txt`:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

5. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Environment Variables

For production, set these environment variables:
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Large PDF files (>10MB) may take longer to process
- Scanned PDFs (images) are not supported - text-based PDFs only
- Some special characters in job descriptions may not be parsed correctly

## 👨‍💻 Author

**Your Name**
- GitHub: [@waqas-404](https://github.com/waqas-404)
- Email: kareemwaqas1@gmail.com

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [scikit-learn](https://scikit-learn.org/)
- [NLTK](https://www.nltk.org/)
- Inspired by the need for better resume optimization tools

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact me via email
- Check the [Wiki](https://github.com/yourusername/ai-resume-analyzer/wiki) for detailed documentation

---

⭐ **If you find this project helpful, please give it a star!** ⭐

Made with ❤️ and Django
