FROM ubuntu:latest

# Install python and pip using miniconda
RUN apt-get -qq update && apt-get -qq -y install bzip2 wget zip \
    && wget -q https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda update conda \
    && conda create -n env python=3.7 \
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
    && wget -q https://www.dropbox.com/s/roms89xbngg1sn4/t-vex-models.zip?dl=1 -O /tvecs/data/models/t-vex-models.zip \
    && unzip /tvecs/data/models/t-vex-models.zip -d /tvecs/data/models/ \
    && apt-get -qq -y remove unzip

# Install python dependencies
SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]
COPY requirements.txt requirements-test.txt /tvecs/
RUN pip install wheel \
    && pip install -r /tvecs/requirements.txt \
    && pip install -r /tvecs/requirements-test.txt \
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
CMD ["conda", "run", "--no-capture-output", "-n", "env", "python", "-m", "tvecs.visualization.server"]

