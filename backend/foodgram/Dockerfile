FROM python:3.8-slim
WORKDIR /app
COPY .  ./
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:5000" ]
