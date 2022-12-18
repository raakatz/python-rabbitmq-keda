FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

USER 1001

CMD ["python3", "-u", "app.py"]

