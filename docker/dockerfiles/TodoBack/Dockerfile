FROM python:3.9-alpine
LABEL authors="haozhe_chen"


WORKDIR /app
COPY ./TodoBack /app

COPY ./docker/dockerfiles/TodoBack/nscacert_combined.pem /certs/
RUN export REQUESTS_CA_BUNDLE='/certs/nscacert_combined.pem'

RUN pip --cert /certs/nscacert_combined.pem install -r requirements.txt

RUN pip install -r requirements.txt
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]



