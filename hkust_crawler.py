import time
import pathlib
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service


class HKUSTCrawler():
    def __init__(self):
        self.service = Service(pathlib.Path.cwd() / 'chromedriver')
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)
        self.username = ''
        self.password = ''

    def log_in(self):
        f = open(pathlib.Path.cwd() / "credentials.txt", "r")
        self.username = f.readline().strip('\n')
        self.password = f.readline().strip('\n')
        print(self.username)
        print(self.password)

    def quit_crawler(self):
        self.driver.quit()

    def job_launcher(self):
        self.driver.get('https://career.ust.hk/web/job_detail.php');
        job_record =[]

        username_input = self.driver.find_element_by_xpath('//*[@id="userNameInput"]')
        username_input.send_keys(self.username)

        password_input = self.driver.find_element_by_xpath('//*[@id="passwordInput"]')
        password_input.send_keys(self.password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="submitButton"]')
        login_btn.click()

        read_btn = self.driver.find_element_by_xpath('//*[@id="chk1"]')
        read_btn.click()

        agree_btn = self.driver.find_element_by_xpath('//*[@id="myform8"]/div/div/input')
        agree_btn.click()

        agree2_btn = self.driver.find_element_by_xpath('//*[@id="myform"]/div/center/input[2]')
        agree2_btn.click()

        time.sleep(2)

        for i in range(25486, 25775):
            try:
                self.driver.get('https://career.ust.hk/web/job_detail.php?jp=' + str(i));
            except:
                continue
            test = self.driver.find_elements_by_class_name('detail-text')
            job = {}

            job['company'] = (test[0].text.split("<br>"))[0]
            job_comb = test[1].text.split("<br>")
            job['job_title'] = (job_comb[0].split('\n'))[0]
            try:
                email = self.driver.find_elements_by_class_name('red_link')
                temp_mail = 'none'
                for item in email:
                    if str(item.get_attribute('href'))[0:7] == 'mailto:':
                        temp_mail = str(item.get_attribute('href'))[7:]
                job['email'] = temp_mail
            except:
                job['email'] = 'none'

            print(job)
            job_record.append(job)
            time.sleep(0.5)
        job_df = pd.DataFrame(job_record)
        return job_df


if __name__ == '__main__':
    ust = HKUSTCrawler()
    ust.log_in()
    job_list = ust.job_launcher()
    job_list.to_csv(pathlib.Path.cwd() / 'job_list.csv')
    ust.quit_crawler()
