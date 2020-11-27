FROM python:3.8.3

WORKDIR /home/parallels/Desktop/test

COPY . /home/parallels/Desktop/test

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["bash","docker_entrypoint.sh"]

CMD python3 main.py
