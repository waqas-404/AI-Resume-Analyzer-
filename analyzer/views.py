from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ResumeAnalysisForm
from .models import ResumeAnalysis
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User

import requests

from django.conf import settings

from .utils import (
    extract_text_from_pdf,
    calculate_similarity,
    find_missing_keywords
)

# Remove these if using internal Django auth
# LOGIN_API_URL = "http://api:8000/auth/login/"
# SIGNUP_API_URL = "http://api:8000/auth/registration/"

def home(request):
    """Home page with upload form"""
    if request.method == 'POST':
        form = ResumeAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            
            try:
                # Extract text from PDF
                resume_text = extract_text_from_pdf(analysis.resume)
                
                if not resume_text:
                    messages.error(request, 'Could not extract text from PDF. Please try another file.')
                    return render(request, 'analyzer/home.html', {'form': form})
                
                # Calculate similarity
                similarity_score, _, _ = calculate_similarity(
                    resume_text, 
                    analysis.job_description
                )
                analysis.similarity_score = similarity_score
                
                # Extract keywords
                job_keywords, matching_keywords, missing_keywords = find_missing_keywords(
                    resume_text,
                    analysis.job_description
                )
                
                analysis.job_keywords = job_keywords
                analysis.resume_keywords = matching_keywords
                analysis.missing_keywords = missing_keywords
                
                analysis.save()
                
                return redirect('results', pk=analysis.pk)
                
            except Exception as e:
                messages.error(request, f'Error processing files: {str(e)}')
                return render(request, 'analyzer/home.html', {'form': form})
    else:
        form = ResumeAnalysisForm()
    
    return render(request, 'analyzer/home.html', {'form': form})

def results(request, pk):
    """Display analysis results"""
    analysis = ResumeAnalysis.objects.get(pk=pk)
    
    # Determine match level
    score = analysis.similarity_score
    if score < 40:
        match_level = 'low'
        match_text = 'Low Match - Needs Improvement'
        recommendation = "Your resume needs significant tailoring to match this job description. Consider incorporating more relevant keywords and highlighting applicable experiences."
    elif score < 70:
        match_level = 'good'
        match_text = 'Good Match - Room for Improvement'
        recommendation = "Your resume aligns fairly well with the job requirements. Fine-tune your resume by emphasizing key skills mentioned in the job description."
    else:
        match_level = 'excellent'
        match_text = 'Excellent Match - Well Aligned'
        recommendation = "Outstanding! Your resume strongly aligns with the job description. You have a great foundation - ensure your cover letter also highlights these matching points."
    
    context = {
        'analysis': analysis,
        'match_level': match_level,
        'match_text': match_text,
        'recommendation': recommendation,
    }
    
    return render(request, 'analyzer/results.html', context)

def history(request):
    """Display analysis history"""
    analyses = ResumeAnalysis.objects.all()[:10]
    return render(request, 'analyzer/history.html', {'analyses': analyses})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Try to find user by email
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            return render(
                request,
                "analyzer/login.html",
                {"error": "Invalid email or password"}
            )

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "analyzer/login.html",
                {"error": "Invalid email or password"}
            )

    return render(request, "analyzer/login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # Basic validation
        if password != password2:
            return render(
                request,
                "analyzer/signup.html",
                {"error": "Passwords do not match"}
            )

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "analyzer/signup.html",
                {"error": "Username already exists"}
            )

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "analyzer/signup.html",
                {"error": "Email already exists"}
            )

        # Validate password length
        if len(password) < 8:
            return render(
                request,
                "analyzer/signup.html",
                {"error": "Password must be at least 8 characters long"}
            )

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
        except Exception as e:
            return render(
                request,
                "analyzer/signup.html",
                {"error": f"Registration failed: {str(e)}"}
            )

    return render(request, "analyzer/signup.html")