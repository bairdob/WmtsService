FROM python:3.9
WORKDIR /WmtsService

COPY ./requirements.txt /WmtsService/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /WmtsService/requirements.txt

COPY ./src /WmtsService

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
