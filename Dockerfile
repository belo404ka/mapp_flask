FROM python:3.8.5
WORKDIR /mapp
COPY requirements.txt /mapp
RUN pip install -r requirements.txt
COPY . .
CMD python app.py