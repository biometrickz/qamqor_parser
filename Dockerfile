FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Almaty

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get -y update \
    && apt-get install -y gcc make \
    && apt-get install -y wget \
    && apt-get install -y gnupg2 \
    && apt-get install -y curl \
    && rm -rf /var/lib/lists/* \
    && rm -rf /var/lib/apt/lists/*s

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/app/chromedriver/

RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY . .

CMD ["python3", "src/main.py"]