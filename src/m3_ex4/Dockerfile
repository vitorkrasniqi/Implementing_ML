FROM python:3.8.3

WORKDIR  /home/vitor/multi_docker_compose





COPY . /home/vitor/multi_docker_compose

RUN pip install -r requirements.txt


RUN pip install sqlalchemy

RUN pip install matplotlib

RUN pip install pandas


# SETUP DB ENVIROMENT VARIABLES
ENV DB_DRIVER='postgres'
ENV DB_HOST='db'
ENV DB_PORT='5432'
ENV DB_USERNAME='admin'
ENV DB_PASSWORD='password1234'
ENV DB_DBNAME='milestone_3'

EXPOSE 5000



CMD   python  m3_ex4_store_data.py





