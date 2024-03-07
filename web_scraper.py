from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv

krs_dataset = pd.DataFrame(columns=['CompanyName', 'Representative'])

driver = webdriver.Chrome()

for krs_num in range(6865, 6900):
    url = 'https://rejestr.io/krs/' + str(krs_num)
    driver.get(url)
    if driver.title != 'Nie znaleziono strony | Rejestr.io':
        company_name = driver.find_element(By.XPATH, '//div[@class="h1_wrapper"]/h1/a').text
        krs_dataset.loc[len(krs_dataset.index)] = [company_name]

driver.close()
krs_dataset.to_csv('krs_data.csv', encoding='utf-8-sig', index=False)


