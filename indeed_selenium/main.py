from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import re
import json
from config import links

browser = webdriver.Chrome()

# try to open company_data.json file if not found company_data_list will be empty
try:
  with open('company_data.json', 'r', encoding='utf-8') as file:
    company_data_list = json.load(file)
except (json.JSONDecodeError, FileNotFoundError):
        company_data_list = []

# for extracing values from strings
def extract_ratings(ratings):
    match = re.search(r'\b\d+(\.\d+)?\b', ratings)
    if match:
        return match.group(0)
    else:
        return "N/A"


def extract_reviews(reviews):
    match = re.search(r'(.+?)Reviews', reviews)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_salaries(salaries):
    match = re.search(r'(.+?)Salaries', salaries)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_jobs(jobs):
    match = re.search(r'(.+?)Jobs', jobs)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_approval(approval):
    match = re.search(r'(\d+%)', approval)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_founded(founded):
    match = re.search(r'(\d+)', founded)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_company_size(company_size):
    match = re.search(r'Company size(.+)', company_size)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_revenue(revenue):
    match = re.search(r'Revenue(.+)', revenue)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_industry(industry):
    match = re.search(r'Industry(.+)', industry)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_headquarters(headquarters):
    match = re.search(r'Headquarters(.+)', headquarters)
    if match:
        return match.group(1)
    else:
        return "N/A"


def extract_title_jobs(job):
    match = re.search(
        r"([a-zA-Z\s,]+)(\d+)", job)
    if match:
        title = match.group(1).strip()
        jobs = int(match.group(2))
        return {'title': title, 'jobs': jobs}
    else:
        return "N/A"


def extract_title_salary(salary):
    match = re.search(r'([a-zA-Z\s]+)\$([\d,]+\.\d{2}|\d+(?:,\d{3})*)(?: per (hour|year|month))?', salary)
    if match:
        job_title = match.group(1).strip()
        salary_amount = match.group(2).strip()
        salary_type = match.group(3) or "year"  # Default to "year" if not specified
        return {'title': job_title, 'salary': f"${salary_amount} per {salary_type}"}
    else:
        return "N/A"

# find and click next
def navigate_to_next_page():
  # click accept privacy policy and terms button if it exists
  try:
    cookies_button = browser.find_element(By.CSS_SELECTOR,"button.gnav-CookiePrivacyNoticeButton[data-gnav-element-name='CookiePrivacyNoticeOk']")
  except Exception as e:
    cookies_button = None
  
  if cookies_button:
    cookies_button.click() 

  # click next button if it exists
  try:
      next = browser.find_element(By.LINK_TEXT, 'Next')
      next.click()
      return True
  except NoSuchElementException as e:
      return False 
  except Exception as e:
      print(f"Error: {e}")
      return False


def scrape_current_page():
    # convert into html
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # select all relevent li tags
    list_companies = soup.select('li h2.css-auuv2u.e1tiznh50 a')
    for indv_companies in list_companies:
        availabe_jobs = {}
        company_salaries = {}
        href = indv_companies.get('href')

        # check for duplicates
        found = any(item['link'] ==
                        f"https://www.indeed.com{href}" for item in company_data_list)
       
        if not found:
          #open link in new tab
          new_tab_script = f'window.open("https://www.indeed.com{href}", "_blank");'
          browser.execute_script(new_tab_script)
          # switch to recently opened window
          browser.switch_to.window(browser.window_handles[-1])
          time.sleep(10)
          # convert into html
          page_source = browser.page_source
          soup = BeautifulSoup(page_source, 'html.parser')
          
          # click accept privacy policy and terms button if it exists
          try:
              cookies_button = browser.find_element(By.CSS_SELECTOR,"button.gnav-CookiePrivacyNoticeButton[data-gnav-element-name='CookiePrivacyNoticeOk']")
          except Exception as e:
              cookies_button = None
          
          if cookies_button:
              cookies_button.click()
          # try:
          #     company_name = soup.find(
          #         'div', {'class': 'css-5lduno e37uo190'}).text
          # except Exception as e:
          #     company_name = soup.find('div',{'class':'css-19rjr9w e1wnkr790'}).text
          try:
              company_name = soup.find('div',itemprop='name').text
          except Exception as e:
              company_name = "N/A"
          try:
              work_wellbeing = soup.find(
                  'div', class_='css-1cosc8r e37uo190').find('span').text
          except Exception as e:
              work_wellbeing = "N/A"
          try:
              ratings = soup.find('div', class_='css-1bxh0bx e37uo190').text
          except Exception as e:
              ratings = "N/A"
          try:
              reviews = soup.find(
                  'li', {'data-tn-element': 'reviews-tab', 'class': 'css-gme78o eu4oa1w0'}).text
          except Exception as e:
              reviews = "N/A"
          try:
              salaries = soup.find(
                  'li', {'data-tn-element': 'salaries-tab', 'class': 'css-gme78o eu4oa1w0'}).text
          except Exception as e:
              salaries = "N/A"
          try:
              jobs = soup.find(
                  'li', {'data-tn-element': 'jobs-tab', 'class': 'css-gme78o eu4oa1w0'}).text
          except Exception as e:
              jobs = "N/A"
          try:
              ceo = soup.find('span', class_="css-1w0iwyp e1wnkr790").text
          except Exception as e:
              ceo = "N/A"
          try:
              ceo_performance_approval = soup.find(
                  'span', class_="css-4oitjw e1wnkr790").text
          except Exception as e:
              ceo_performance_approval = "N/A"
          try:
              founded = soup.find(
                  'li', {'data-testid': 'companyInfo-founded', 'class': 'css-1wsezwx e37uo190'}).text
          except Exception as e:
              founded = "N/A"
          try:
              company_size = soup.find(
                  'li', {'data-testid': 'companyInfo-employee', 'class': 'css-1wsezwx e37uo190'}).text
          except Exception as e:
              company_size = "N/A"
          try:
              revenue = soup.find(
                  'li', {'data-testid': 'companyInfo-revenue', 'class': 'css-1wsezwx e37uo190'}).text
          except Exception as e:
              revenue = "N/A"
          try:
              industry = soup.find(
                  'li', {'data-testid': 'companyInfo-industry', 'class': 'css-1wsezwx e37uo190'}).text
          except Exception as e:
              industry = "N/A"
          try:
              headquarters = soup.find('li', {
                  'data-testid': 'companyInfo-headquartersLocation', 'class': 'css-1wsezwx e37uo190'}).text
          except Exception as e:
              headquarters = "N/A"
          try:
              summary = soup.find(
                  'div', {'class': 'css-y6ifcp eu4oa1w0'}).text
          except Exception as e:
              summary = "N/A"

      # close popup
          try:
              sticky_button = browser.find_element(
                  By.CSS_SELECTOR, 'button[data-testid="sticky-jobs-cta-close"]')
          except Exception as e:
              sticky_button = None

          if sticky_button:
              sticky_button.click()
              time.sleep(2)

          # load more jobs by clicking on more jobs button
          try:
              more_jobs_by_title = browser.find_elements(
                  By.CSS_SELECTOR, 'div.css-15lwuw4.eu4oa1w0 button[data-tn-action-click="true"]')
          except Exception as e:
              more_jobs_by_title = None

          if more_jobs_by_title:
              for indv_buttons in more_jobs_by_title:
                  indv_buttons.click()
                  time.sleep(2)
              # parse jobs data
              page_source = browser.page_source
              soup = BeautifulSoup(page_source, 'html.parser')
              list_jobs_by_title = soup.select('div.css-am958r.e37uo190')
              for indv_list_jobs_by_title in list_jobs_by_title:
                  job_data = extract_title_jobs(indv_list_jobs_by_title.text)
                  if job_data != "N/A":
                      availabe_jobs[job_data['title']] = job_data['jobs']

          # if no more jobs parse it as it is
          else:
              list_jobs_by_title = soup.select('div.css-am958r.e37uo190')
              for indv_list_jobs_by_title in list_jobs_by_title:
                  job_data = extract_title_jobs(indv_list_jobs_by_title.text)
                  if job_data != "N/A":
                      availabe_jobs[job_data['title']] = job_data['jobs']
          # parse salary data
          salaries_list = soup.select(
              'div.cmp-SalaryCategoryCard.css-n5zvfs.e37uo190')
          for indv_salary in salaries_list:
              salary_data = extract_title_salary(indv_salary.text)
              if salary_data != "N/A":
                  company_salaries[salary_data['title']] = salary_data['salary']

          company_data = {
              "link": f"https://www.indeed.com{href}",
              "company_name": company_name,
              "work_wellbeing_rating": extract_ratings(work_wellbeing),
              "ratings": extract_ratings(ratings),
              "reviews": extract_reviews(reviews),
              "salaries": extract_salaries(salaries),
              "jobs": extract_jobs(jobs),
              "ceo": ceo,
              "ceo_performance_approval": extract_approval(ceo_performance_approval),
              "founded": extract_founded(founded),
              "company_size": extract_company_size(company_size),
              "revenue": extract_revenue(revenue),
              "industry": extract_industry(industry),
              "headquarters": extract_headquarters(headquarters),
              "summary": summary,
              "availabe_jobs": availabe_jobs,
              "company_salaries": company_salaries
          }
          company_data_list.append(company_data)
          browser.close()
          browser.switch_to.window(browser.window_handles[0])
          # write data 
          with open('company_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(company_data_list, json_file, indent=2, ensure_ascii=False)
    
    # write to json file


# send request to each links
for indv_link in links:
  browser.get(f"https://www.indeed.com/companies/{indv_link}")   
  while True:
      scrape_current_page()
      time.sleep(5)
      if not navigate_to_next_page():
          break
