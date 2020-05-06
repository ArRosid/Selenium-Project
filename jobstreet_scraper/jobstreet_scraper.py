from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os


# initialize start time
start_time = time.time()

df = pd.DataFrame(columns=['Title', 'Company', 'Location', 'Salary', 'Posted'])

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

while True:
    # get all jobs
    all_jobs = browser.find_elements_by_xpath('//div[@class="panel "]')
    for job in all_jobs:
        title = job.find_element_by_xpath('.//a[@class="position-title-link"]/h2').text
        try:
            company = job.find_element_by_xpath('.//a[@class="company-name"]/span').text
        except:
            company = "Company Confidential"

        location = job.find_element_by_xpath('.//li[@class="job-location"]/span').text
        try:
            salary = job.find_element_by_xpath('.//li[@id="job_salary"]/font').text
        except:
            salary = ''

        posted = job.find_element_by_xpath('.//span[@class="job-date-text text-muted"]').text

        # if title:
        data = {}
        data['Title'] = title,
        data['Company'] = company,
        data['Location'] = location,
        data['Salary'] = salary
        data['Posted'] = posted
        print(data)

        df = df.append(data, ignore_index=True)

    # go to next page
    time.sleep(5)
    try:
        next_page = browser.find_element_by_id('page_next')
    except:
        next_page = None

    if next_page:
        next_page.click()
    else:
        break


# set the index to start from 1
df.index += 1

df.to_csv('jobstreet_scraper/programmer_jobs_all_pages.csv')

elapsed_time = time.time() - start_time
print(f"The program is done in {elapsed_time} seconds")
print(df.head())
