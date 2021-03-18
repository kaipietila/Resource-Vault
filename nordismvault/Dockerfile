FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=nordismvault.settings
RUN mkdir /nordismvault
WORKDIR /nordismvault
COPY requirements.txt /nordismvault/
RUN pip install -r requirements.txt
COPY . /nordismvault/