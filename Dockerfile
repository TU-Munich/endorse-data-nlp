FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m spacy download en
RUN python -m spacy download de
# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;
COPY . .
EXPOSE 3002
RUN [ "chmod", "+x", "start.sh" ]
CMD [ "sh", "./start.sh" ]
CMD [ "python", "./main.py" ]
