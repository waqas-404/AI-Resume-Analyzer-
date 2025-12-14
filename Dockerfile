FROM python:3.11.9-slim-bookworm

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install NLTK and download resources (updated to punkt_tab and averaged_perceptron_tagger_eng)
RUN python -m pip install --no-cache-dir nltk
RUN python -m nltk.downloader punkt_tab stopwords averaged_perceptron_tagger_eng -d /usr/local/nltk_data

COPY . /app

EXPOSE 8000