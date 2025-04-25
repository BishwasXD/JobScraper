FROM mcr.microsoft.com/playwright/python:v1.37.0-focal
WORKDIR /src
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
RUN playwright install
CMD [ "python", "src/spiders/scraper.py"]
