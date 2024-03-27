FROM python:3.11-slim
WORKDIR /usr/src/app
COPY Client.py client.py
#RUN pip install --no-cache-dir fastapi uvicorn
EXPOSE 8000
CMD ["python3", "client.py"]
