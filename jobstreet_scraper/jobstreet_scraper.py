from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os

chrome_options = Options()
chrome_options.add_argument('--incognito')
browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

url = 'https://www.jobstreet.co.id/'
browser.get(url)

time.sleep(5)

# click login
login_button = browser.find_element_by_xpath('//button[@id="header-login-button"]')
login_button.click()

time.sleep(5)

# login using username and password
browser.find_element_by_id('login-email').send_keys(os.environ['JOBSTREET_USER'])
browser.find_element_by_id('login-password').send_keys(os.environ['JOBSTREET_PASSWORD'])
browser.find_element_by_id('login_btn').click()

# search for programmer jobs
browser.find_element_by_id('search_box_keyword').send_keys('programmer')
browser.find_element_by_id('header_searchbox_btn').click()
time.sleep(5)

# sort by date
select = Select(browser.find_element_by_id('sort_result'))
select.select_by_visible_text('Date')
time.sleep(5)

# get all jobs
all_jobs = browser.find_elements_by_xpath('//div[@class="panel "]')
for job in all_jobs:
    title = job.find_element_by_xpath('.//a[@class="position-title-link"]').text
    try:
        company = job.find_element_by_xpath('.//a[@class="company-name"]/span').text
    except:
        company = "Company Confidential"

    location = job.find_element_by_xpath('.//li[@class="job-location"]/span').text
    salary = job.find_element_by_xpath('.//li[@id="job_salary"]/font').text

    print({
        'title': title,
        'company': company,
        'location': location,
        'salary': salary
    })
