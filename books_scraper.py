from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

chrome_options = Options()
chrome_options.add_argument('--incognito')
browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

df = pd.DataFrame(columns=['Title', 'Image', 'Price', 'Star'])
url = 'http://books.toscrape.com/'
browser.get(url)
for _ in range(2):
    books = browser.find_elements_by_xpath('//article[@class="product_pod"]')
    for book in books:
        data = {}
        data['Title'] = book.find_element_by_xpath('.//img').get_attribute('alt')
        data['Image'] = book.find_element_by_xpath('.//img').get_attribute('src')
        data['Price'] = book.find_element_by_xpath('.//p[@class="price_color"]').text
        data['Star'] = book.find_element_by_xpath('.//p').get_attribute('class').split()[-1]

        df = df.append(data, ignore_index=True)

    next_page = browser.find_element_by_xpath('//li[@class="next"]/a')
    if next_page:
        next_page.click()

browser.close()
# set the index to start from 1
df.index += 1
df.to_csv('books.csv')
