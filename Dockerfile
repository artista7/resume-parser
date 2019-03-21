FROM python:3.6

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader averaged_perceptron_tagger
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords

COPY . /app

# for a flask server
EXPOSE 5000

ENTRYPOINT ["gunicorn"]

CMD ["-b", "0.0.0.0:5000", "app:app"]
