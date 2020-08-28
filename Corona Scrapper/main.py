from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--headless')
firefox_options.add_argument('window-size=1920,1080')
firefox_options.add_argument('--disable-gpu')
driver = webdriver.Firefox(firefox_options=firefox_options)

site_url = "https://www.coronatracker.com/country/india/"

uClient = uReq(site_url)  # requesting the webpage from internet
sitePage = uClient.read()  # reading the webpage
uClient.close()

site_html = bs(sitePage, "html.parser")  # parsing the webpage as html

review_url = "https://www.coronatracker.com/country/india/"
driver.get(review_url)
driver.implicitly_wait(30)
source = driver.page_source

html = bs(source, "html.parser")  # parsing the webpage as HTML

bigboxes = html.findAll("div", {
    "class": "flex flex-wrap -mx-2"})

confirmed_cases = bigboxes[0].find("p", {
    "class": "text-2xl font-bold text-red-600"}).text.strip()

recovered_cases = bigboxes[0].find("p", {
    "class": "text-2xl font-bold text-green-600"}).text.strip()

death_cases = bigboxes[0].find("p", {
    "class": "text-2xl font-bold text-gray-600"}).text.strip()

cases_icu = bigboxes[0].find("div", {
    "class": "text-gray-900 font-bold text-2xl mb-2"}).text.strip()

print("!-----INDIA CORONA OVERVIEW-----!")
print("TOTAL CONFIRMED CASES:", confirmed_cases)
print("TOTAL RECOVERED CASES:", recovered_cases)
print("TOTAL DEATHS:", death_cases)
print("CRITICAL CASES TREATED IN ICU:", cases_icu)

message = "TOTAL CONFIRMED CASES: " + confirmed_cases + "\nTOTAL RECOVERED CASES: " + recovered_cases + "\nTOTAL DEATHS: " + death_cases + "\nCRITICAL CASES TREATED IN ICU: " + cases_icu

from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast(title="!-----INDIA CORONA OVERVIEW-----!",
                   msg=message,
                   icon_path=None,
                   duration=10)
