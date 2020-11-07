FROM python:3.8.3

WORKDIR  /home/vitor/Deeplearning





COPY . /home/vitor/Deeplearning

RUN pip install -r resources/requirements.txt


CMD   python  src/main.py





