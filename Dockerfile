FROM seleniumbase/ubuntu:latest

WORKDIR /qa
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["pytest", "tests/", "--headless", "-m", "not known_bug", "--html=reports/report.html", "--self-contained-html"]