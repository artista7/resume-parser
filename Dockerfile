FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader averaged_perceptron_tagger
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords

COPY . /app

ENTRYPOINT ["gunicorn"]

CMD ["-b", "0.0.0.0:5000", "app:app"]
