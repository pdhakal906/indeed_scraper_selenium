from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


strings = []

browser = webdriver.Firefox()

browser.get('https://www.indeed.com/companies')
browser.find_element(
    By.CSS_SELECTOR, "a[data-tn-element='cmp-Industry-link']").click()

def open_dropdown():
  browser.find_element(
      By.CSS_SELECTOR, "button[data-tn-component='DropdownInput']").click()
def open_location_dropdown():
  browser.find_element(By.ID, "location-dropdown-toggle-button").click()

def extract():
  open_dropdown()
  for i in range(1, 141):
    # skip the industries that do not have data available
    if i == 110 or i == 111 or i == 93 or i == 122:
       continue
    browser.find_element(By.ID, f"downshift-0-item-{i}").click()
    time.sleep(5)
    open_location_dropdown()
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    industry = soup.find(
                  'span', {'class': 'css-y8rzho e1wnkr790'}).text
    list_locations = soup.select('li.css-777tmm.ehvvxyn0')

    for indv_location in list_locations[1:]:
        string = f"best-{industry.replace(' ', '-')
                         }-companies-in-{indv_location.text.split(' - ')[0].replace(' ', '-')}"
        strings.append(string)
       
    open_dropdown()
    time.sleep(5)

extract()

with open('config.py', 'w') as file:
    file.write('links = [\n')
    for links in strings:
        file.write(f'"{links}", \n')
    file.write(']\n')