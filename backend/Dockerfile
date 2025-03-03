FROM python:3.10-slim

WORKDIR /

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

# Copy and configure entrypoint
COPY entrypoint.sh entrypoint.sh
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
CMD gunicorn --bind 0.0.0.0:${PORT:-8000} backend.wsgi:application