FROM python:3.11
ADD bot.py .
ADD requirements.txt .
RUN apt-get update
RUN apt-get install -y redis
RUN pip install --upgrade pip
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip install --no-index -f /usr/src/app/wheels -r requirements.txt && rm -rf /usr/src/app/wheels
CMD ["python", "./bot.py"]