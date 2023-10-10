FROM python:3.8-slim

WORKDIR ./

EXPOSE 80
COPY ./requirements.txt ./requirements.txt

RUN apt-get update \
    && apt-get -y install gcc \
    && apt-get clean \
    && apt-get -y install libpcap-dev libpq-dev tk
RUN apt-get update
RUN apt-get -y install ffmpeg libsm6 libxext6
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt \
    && rm -rf /root/.cache/pip
ENV PYTHONUNBUFFERED=1

COPY . ./
CMD ["python3", "consumer.py"]