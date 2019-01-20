FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m spacy download en
RUN python -m spacy download de
COPY . .
EXPOSE 3002
RUN [ "chmod", "+x", "start.sh" ]
CMD [ "sh", "./start.sh" ]
CMD [ "python", "./main.py" ]
