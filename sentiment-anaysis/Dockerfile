FROM python:3.6-slim
ADD . /code
WORKDIR /code
RUN pip install nltk
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader words
RUN python -m nltk.downloader wordnet
RUN pip install textblob
RUN python -m textblob.download_corpora



RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "sentiment_Analysis.py"]

