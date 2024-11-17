FROM python:3.9-slim
WORKDIR /app
COPY main.py /app/
COPY .env /app/ 
RUN pip install fastapi uvicorn python-dotenv
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
