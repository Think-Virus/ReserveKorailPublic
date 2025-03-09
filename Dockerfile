FROM python:3.11


# git clone 실행
WORKDIR /home/
RUN git clone git@github.com:chunccc1004/reservationKorail.git
WORKDIR /home/reservationKorail/
RUN pip install -r requirements.txt


# selenium 실행을 위한 환경 설정
RUN apt-get -y update && \
    apt install wget && \
    apt install unzip \
# chrome 설치 -> 현재 123.0.6312.86으로 설치됨
RUN RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
# chrome driver 설치
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chromedriver-linux64.zip
RUN mkdir chrome
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome

CMD ["bash", "-c", "python -u __init__.py"]