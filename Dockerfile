FROM python:3.9

WORKDIR /app

COPY . .

# 🔥 IMPORTANT
COPY artifacts/ artifacts/

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
