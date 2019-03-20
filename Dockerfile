FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt
RUN python -m nltk.downloader averaged_perceptron_tagger
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords

COPY . /app

CMD [ "gunicorn app:app" ]
