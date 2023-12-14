FROM python:3-alpine3.11
ADD bot.py .
ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN pip install --no-index -f /usr/src/app/wheels -r requirements.txt && rm -rf /usr/src/app/wheels
CMD ["python", "./bot.py"]