FROM python:3

LABEL Maintainer="Harish Kumar V"

WORKDIR /usr/app/src

RUN pip3 install flask pandas flasgger

COPY app.py .

COPY . /usr/app/src

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "9000"]
