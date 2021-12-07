FROM nvidia/cuda:11.0-runtime-ubuntu20.04

RUN apt-get update && apt-get install -y python3.7 python3-pip

COPY . .

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "ocr:app",  "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "1", "--timeout", "380"]