FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /api
COPY ./requirements.txt /api/requirements.txt
RUN pip install -r /api/requirements.txt
COPY . /api
CMD ['python', 'manage.py', 'runserver', '127.0.0.1:8000']

