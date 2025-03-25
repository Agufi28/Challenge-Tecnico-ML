FROM python:3.12.6

WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app

CMD ["python","-m","fastapi", "run", "main.py", "--port", "80"]



