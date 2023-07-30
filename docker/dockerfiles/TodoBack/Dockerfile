FROM python:3.9-alpine
LABEL authors="haozhe_chen"


WORKDIR /app
COPY ./TodoBack /app

RUN pip install -r requirements.txt
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]



