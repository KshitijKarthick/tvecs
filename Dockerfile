FROM ubuntu:latest

# Install python and pip
RUN apt-get update \
 && apt-get -y install python3-pip python3-dev git wget \
 && apt-get -y install gfortran libopenblas-dev liblapack-dev \
 && apt-get -y autoremove \
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/KshitijKarthick/tvecs.git /tvecs

RUN pip install -r /tvecs/requirements.txt

# Add our code
WORKDIR /tvecs

# Expose for cherrypy
EXPOSE 5000

# Run the app.
CMD ["python", "-m", "tvecs.visualization.server"]
