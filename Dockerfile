FROM python:latest

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app/

RUN chmod +x /app/main.sh

CMD ["./main.sh"]