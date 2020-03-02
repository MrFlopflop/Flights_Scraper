import smtplib
from time import sleep
from selenium import webdriver
from secrets import email, password

cheapest = [9999, None]

driver = webdriver.Chrome()

class Flight:
    def __init__(self, dict, cheapest):
        self.toDates = dict['toDates']
        self.fromDates = dict['fromDates']
        self.cheapest = cheapest
        self.URL1 = dict['url1']
        self.middleBit = dict['middleBit']
        self.URL2 = dict['url2']
        self.to = dict['to']
        self.type = dict['type']
        self.price = dict['price']

    def check_price(self, toDate, fromDate):
        try:
            price = driver.find_element_by_css_selector('.gws-flights-results__cheapest-price').text
            converted_price = int(price[2:])
            if self.cheapest[0] <= converted_price:
                return self.cheapest
            else:
                return [converted_price, [toDate, fromDate]]
        except:
            button = driver.find_element_by_xpath(
                '//*[@id="flt-app"]/div[2]/main[4]/div[7]/div[2]/div/div[2]/fill-button')
            button.click()
            sleep(0.5)
            self.check_price(toDate, fromDate)

    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)

        subject = 'Goedkope vlucht'
        if self.type == 'enkele':
            body = "Er is een " + self.type + " vlucht van " + str(self.cheapest[0]) + " euro naar " + self.to + " \n"\
               + self.URL1 + self.cheapest[1][0] + self.URL2
        elif self.type == 'retour':
            body = "Er is een " + self.type + " vlucht van " + str(self.cheapest[0]) + " euro naar " + self.to + " \n" \
                   + self.URL1 + self.cheapest[1][0] + self.middleBit + self.cheapest[1][1] + self.URL2

        msg = f'Subject: {subject}\n\n{body}'
        server.sendmail(
            email,
            email,
            msg
        )
        server.quit()

    def scrape(self):
        driver.implicitly_wait(15)
        if self.type == 'enkele':
            for toDate in self.toDates:
                driver.get(self.URL1 + toDate + self.URL2)
                sleep(0.5)
                self.cheapest = self.check_price(toDate, None)
        elif self.type == 'retour':
            for toDate in self.toDates:
                for fromDate in self.fromDates:
                    driver.get(self.URL1 + toDate + self.middleBit + fromDate + self.URL2)
                    sleep(0.5)
                    self.cheapest = self.check_price(toDate, fromDate)
        if self.cheapest[0] < self.price:
            self.send_mail()
        print(self.to, self.cheapest)

driver.quit()
