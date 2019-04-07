#FROM ubuntu:16.04
FROM continuumio/miniconda3
ADD . /code	
WORKDIR /code

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    python-pip \
    libgl1-mesa-glx

#    python2.7 \
#    python2.7-dev \
#    ssh \
#    && apt-get autoremove \
#    && apt-get clean
	
RUN pip install --upgrade pip
RUN pip install pillow
RUN pip install matplotlib
RUN pip install numpy
RUN pip install -r requirements.txt

#RUN pip install wordcloud-1.3.tar.gz
#RUN pip install wordcloud
#RUN python setup.py install

#RUN python -m pip install wordcloud-1.5.0-cp27-cp27mu-manylinux1_x86_64

RUN conda install -c conda-forge wordcloud 
RUN conda install -c conda-forge matplotlib

#CMD ["python", "-m pip install wordcloud-1.5.0-cp27-cp27mu-manylinux1_x86_64"]
#CMD ["conda", "install -c conda-forge wordcloud"]
#CMD ["pip", "install wordcloud-1.3.tar.gz"]

CMD ["python", "wordcloudrun.py"]


