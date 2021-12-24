FROM python:3.6
WORKDIR /fastapi
COPY requirements.txt /fastapi
RUN pip install -r requirements.txt
COPY ./app app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]