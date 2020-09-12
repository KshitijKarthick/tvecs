FROM ubuntu:latest

# Install python and pip using miniconda
RUN apt-get -qq update && apt-get -qq -y install curl bzip2 wget \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3.6 \
    && conda update conda \
    && apt-get -qq -y remove curl bzip2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes

# Download Bilingual corpora
RUN mkdir -p /tvecs/data/bilingual_dictionary \
    && wget -q https://www.dropbox.com/s/vphpv025s8mkphr/english_hindi_train_bd?dl=1 -O /tvecs/data/bilingual_dictionary/english_hindi_train_bd \
    && wget -q https://www.dropbox.com/s/erba49z64ef6nkp/hindi_english_train_bd?dl=1 -O /tvecs/data/bilingual_dictionary/hindi_english_train_bd

# Download models
RUN mkdir -p /tvecs/data/models \
    && wget -q https://www.dropbox.com/s/a6mh6f073czk0vg/t-vex-english-model?dl=1 -O /tvecs/data/models/t-vex-english-model \
    && wget -q https://www.dropbox.com/s/wouwsdwuobcvs0b/t-vex-hindi-model?dl=1 -O /tvecs/data/models/t-vex-hindi-model

# Install python dependencies
COPY requirements.txt requirements-test.txt /tvecs/
RUN pip3 install wheel \
    && pip3 install -r /tvecs/requirements.txt \
    && pip3 install -r /tvecs/requirements-test.txt \
    && mkdir -p tvecs/data/models

# Download nltk data for tokenizing
RUN python3 -c "import nltk;nltk.download('punkt')"

# Copy package files into the image
COPY setup.py setup.cfg conf.py config.json /tvecs/
COPY tvecs/ /tvecs/tvecs
COPY tests /tvecs/tests

# Add our code
WORKDIR /tvecs

# Expose for cherrypy
EXPOSE 5000

# Run the app.
CMD ["python3", "-m", "tvecs.visualization.server"]
