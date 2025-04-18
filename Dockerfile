FROM python:3.12
WORKDIR /src
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "src/app/main.py"]
