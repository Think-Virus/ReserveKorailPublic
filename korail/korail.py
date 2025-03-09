import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait

is_aws = True  # False로 바꾸고 push X


class Korail:
    def __init__(self):
        super().__init__()
        self.member_number = ""
        self.password = ""
        self.driver = None
        self.is_login = False

    def login(self):
        # 옵션 생성
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        # aws에서 사용할 service 설정
        if is_aws:
            CHROMEDRIVER_PATH = "/usr/src/chrome/chromedriver"
            service = Service(executable_path=CHROMEDRIVER_PATH)
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)

        self.driver.get("http://www.letskorail.com/korail/com/login.do#")
        self.driver.find_element(By.ID, "txtMember").send_keys(self.member_number)
        pw_form = self.driver.find_element(By.ID, "txtPwd")
        pw_form.send_keys(self.password)
        pw_form.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            alert_obj = self.driver.switch_to.alert
            alert_obj.accept()
            return
        except:
            pass
        time.sleep(2)

        windowList = self.driver.window_handles

        for i in windowList:
            if i != windowList[0]:
                self.driver.switch_to.window(i)
                self.driver.close()

        self.driver.switch_to.window(windowList[0])

        # self.driver.find_element(By.XPATH,
        #                          '//*[@id="res_cont_tab01"]/form/div/fieldset/p/a/img').click()  # 예매 화면으로 이동
        self.driver.get("https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do")
        self.is_login = True

    def fill_departure_city(self, city):
        dep_city = self.driver.find_element(By.ID, "start")
        dep_city.clear()
        dep_city.send_keys(city)
        dep_city.send_keys(Keys.RETURN)

    def fill_arrival_city(self, city):
        arr_city = self.driver.find_element(By.ID, "get")
        arr_city.clear()
        arr_city.send_keys(city)
        arr_city.send_keys(Keys.RETURN)

    def fill_year(self, year):
        select_year = Select(self.driver.find_element(By.ID, "s_year"))
        select_year.select_by_value(year)

    def fill_month(self, month):
        select_month = Select(self.driver.find_element(By.ID, "s_month"))
        select_month.select_by_value(month)

    def fill_day(self, day):
        select_day = Select(self.driver.find_element(By.ID, "s_day"))
        select_day.select_by_value(day)

    def fill_hour(self, hour):
        select_hour = Select(self.driver.find_element(By.ID, "s_hour"))
        select_hour.select_by_value(hour)

    def search_seats(self, tele):
        self.driver.find_element(By.CSS_SELECTOR, ".btn_inq > a:nth-child(1) > img:nth-child(1)").click()
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass

        windowList = self.driver.window_handles

        for i in windowList:
            if i != windowList[0]:
                self.driver.switch_to.window(i)
                self.driver.close()

        self.driver.switch_to.window(windowList[0])

        while True:
            try:
                wait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH,
                                                                             '// *[ @ id = "tableResult"] / tbody / tr[1] / td[3]')))
                print("break")
                break
            except:
                print("continue")
                continue
        schedule_list = []
        for order_no in range(1, 11):
            try:
                schedule_list.append(str(order_no))
                schedule_list.append(
                    self.driver.find_element(By.XPATH, '//*[@id="tableResult"]/tbody/tr[%s]/td[3]' % order_no).text)
                schedule_list.append(
                    self.driver.find_element(By.XPATH, '//*[@id="tableResult"]/tbody/tr[%s]/td[4]' % order_no).text)
                schedule_list.append(self.driver.find_element(By.XPATH,
                                                              '//*[@id="tableResult"]/tbody/tr[%s]/td[6]/img' % order_no).get_attribute(
                    'alt'))
                schedule_list.append("------------")
                print(schedule_list)
            except:
                schedule_list.append("기차편없음")
                schedule_list.append("------------")
        full_information = '\n'.join(schedule_list)

        departure_hour_min_msg = {'text': '결과'}
        from tele.telegram import Telegram
        Telegram.start_telegram(tele, departure_hour_min_msg, full_information)

    def try_seats(self, tele, order):
        try:
            from tele.telegram import Telegram
            count = 0
            unavailable_seats = None

            Telegram.start_telegram(tele, {'text': '예약시작'})

            while True:
                if unavailable_seats == "예약하기":
                    try:
                        wait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                                     '//*[@id="tableResult"]/tbody/tr[%s]/td[6]/a/img' % order))).click()
                    except:
                        continue

                    time.sleep(3)
                    Telegram.start_telegram(tele, {'text': '예약완료'})
                    try:
                        popup_iframe = self.driver.find_element(By.XPATH, '//*[@id="embeded-modal-traininfo"]')
                        self.driver.switch_to.frame(popup_iframe)
                        self.driver.find_element(By.LINK_TEXT, '닫기').click()
                        self.driver.implicitly_wait(1)
                    finally:
                        time.sleep(3)
                        alert = self.driver.switch_to.alert
                        alert.accept()
                        time.sleep(1)
                else:
                    try:
                        unavailable_seats = wait(self.driver, 3).until((EC.visibility_of_element_located((By.XPATH,
                                                                                                          '//*[@id="tableResult"]/tbody/tr[%s]/td[6]/a/img' % order)))).get_attribute(
                            'alt')
                    except:
                        self.driver.find_element(By.CSS_SELECTOR,
                                                 ".btn_inq > a:nth-child(1) > img:nth-child(1)").click()
                        try:
                            alert = self.driver.switch_to.alert
                            alert.accept()
                        except:
                            pass
                        while True:
                            try:
                                wait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH,
                                                                                             '// *[ @ id = "tableResult"] / tbody / tr[1] / td[3]')))
                                print("break")
                                break
                            except:
                                print("continue")
                                continue
                        count += 1
                        if count % 100 == 0:
                            Telegram.start_telegram(tele, {'text': '예약중'})
                        print(count)

                        continue

                    self.driver.find_element(By.CSS_SELECTOR, ".btn_inq > a:nth-child(1) > img:nth-child(1)").click()
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except:
                        pass
                    wait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                                 '// *[ @ id = "tableResult"] / tbody / tr[1] / td[3]')))
                    count += 1
                    if count % 100 == 0:
                        Telegram.start_telegram(tele, {'text': '예약중'})
                    print(count)
        except:
            Telegram.start_telegram(tele, {'text': '오류가 발생하여 예약을 실패하였습니다.'})
