FROM python:3.6
WORKDIR /fastapi
COPY requirements.txt /fastapi
COPY ./app /fastapi/app
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]