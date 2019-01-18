FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m spacy download en
RUN python -m spacy download de

COPY . .

CMD [ "python", "./main.py" ]

# Expose ports
EXPOSE 5000