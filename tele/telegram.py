import re
from datetime import datetime

import telepot

import os
from dotenv import load_dotenv

from korail.korail import *


class Telegram:
    chat_id = None

    def __init__(self):
        print("텔레그램 구동합니다")
        load_dotenv()
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.bot = telepot.Bot(self.token)
        self.korail = Korail()
        self.bot.message_loop(self.start_telegram)

        while 1:
            pass

    def start_telegram(self, msg, info=None):
        tel_text = msg['text']
        if 'chat' in msg:
            if 'id' in msg['chat']:
                self.chat_id = msg['chat']['id']

        input_departure = re.compile('출발*')  # 출발 도시
        input_departure_city = re.compile('[^출발]')  # 출발 글자 삭제
        input_arrival = re.compile('도착*')  # 도착 도시
        input_arrival_city = re.compile('[^도착]')  # 도착 글자 삭제
        input_year = re.compile(str(datetime.now().year))  # 년
        input_month = re.compile('[0-9]+월')  # 월
        input_month_number = re.compile("[^월]")  # 월 글자 삭제
        input_day = re.compile('[0-9]+일')  # 일
        input_day_number = re.compile('[^일]')  # 일 글자 삭제
        input_hour = re.compile('[0-9]+시')  # 시
        input_hour_number = re.compile('[^시]')  # 시 글자 삭제
        input_book = re.compile('선택[0-9]')  # 선택
        input_book_number = re.compile('[^선택]')  # 선택 빼기
        input_member_number = re.compile('회원번호*')  # 회원 번호
        input_member_number_core = re.compile('[^회원번호]')  # 회원 번호 삭제
        input_password = re.compile('비밀번호*')  # 비밀 번호
        input_password_core = re.compile('[^비밀번호]')  # 회원 번호 삭제

        if not self.korail.is_login:
            tel_text = str(tel_text).replace(" ", "")
            if input_member_number.match(tel_text):
                member_number = input_member_number_core.findall(tel_text)
                self.korail.member_number = str(''.join(member_number))
                self.bot.sendMessage(self.chat_id, "\n회원 번호가 입력되었습니다.\n다음과 같이 비밀번호를 알려주세요.\nex) 비밀번호 as12345678")
            elif input_password.match(tel_text):
                password = input_password_core.findall(tel_text)
                self.korail.password = str(''.join(password))

                self.bot.sendMessage(self.chat_id, "로그인... 잠시만 기다려주세요")
                self.korail.login()
                if self.korail.is_login:
                    self.bot.sendMessage(self.chat_id, "로그인 완료\n다음과 같이 출발역을 알려주세요.\nex) 출발 광명")
                else:
                    self.bot.sendMessage(self.chat_id, "회원번호나 비밀번호가 틀렸습니다.\n회원번호를 다시 알려주세요.\nex) 회원번호 0540354166")
            else:
                self.bot.sendMessage(self.chat_id, "로그인 되지 않은 상태입니다.\n로그인을 먼저 진행해야 합니다.\n회원번호를 알려주세요.\nex) 회원번호 0540354166")
        elif tel_text == "검색":  # 검색
            self.korail.search_seats(tele=self)
        elif tel_text == "결과":
            self.bot.sendMessage(self.chat_id, info)
        elif tel_text == "예약중":
            self.bot.sendMessage(self.chat_id, "예약 중입니다!")
        elif tel_text == "예약시작":
            self.bot.sendMessage(self.chat_id, "예약을 시작합니다.")
        elif tel_text == "예약완료":
            self.bot.sendMessage(self.chat_id, "예약완료하였습니다. 앱을 통해 확인해보세요.")
        elif input_book.match(tel_text):
            book_order_no = input_book_number.findall(tel_text)
            book_order_no = str(''.join(book_order_no))
            self.korail.try_seats(tele=self, order=book_order_no)
        elif input_departure.match(tel_text):  # 출발역 선택
            departure_city = input_departure_city.findall(tel_text)
            departure_city = ''.join(departure_city)
            self.bot.sendMessage(self.chat_id, departure_city + "\n출발역이 선택되었습니다.\n다음과 같이 도착역을 알려주세요.\nex) 도착 구포")
            self.korail.fill_departure_city(departure_city)
        elif input_arrival.match(tel_text):  # 도착역 선택
            arrival_city = input_arrival_city.findall(tel_text)
            arrival_city = ''.join(arrival_city)
            self.bot.sendMessage(self.chat_id, arrival_city + "\n도착역이 선택되었습니다.\n다음과 같이 출발할 날짜를 알려주세요.\n18일")
            self.korail.fill_arrival_city(arrival_city)
        elif input_year.match(tel_text):  # 출발년도 선택
            self.korail.fill_year(tel_text)
        elif input_month.match(tel_text):  # 출발달 선택
            departure_month = input_month_number.findall(tel_text)
            departure_month = ''.join(departure_month)
            self.korail.fill_month(departure_month)
        elif input_day.match(tel_text):  # 출발일 선택
            departure_day = input_day_number.findall(tel_text)
            departure_day = ''.join(departure_day)
            self.bot.sendMessage(self.chat_id, departure_day + "\n출발일이 선택되었습니다.\n표를 조회합니다.")
            self.korail.fill_day(departure_day)
            self.korail.search_seats(tele=self)
            self.bot.sendMessage(self.chat_id, departure_day + "\n예매할 표를 선택해주세요.\nex)선택 3")
        elif input_hour.match(tel_text):  # 출발시간 선택
            departure_hour = input_hour_number.findall(tel_text)
            departure_hour = ''.join(departure_hour)
            self.korail.fill_hour(departure_hour)
        else:
            self.bot.sendMessage(self.chat_id, "잘못된 입력입니다.")
