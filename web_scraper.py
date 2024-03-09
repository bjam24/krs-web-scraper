import time as t
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv

krs_dataset = pd.DataFrame(columns=['OrganizationName'])

driver_organizations = webdriver.Chrome()
driver_representatives = webdriver.Chrome()
driver_connections = webdriver.Chrome()

for krs_num in range(6865, 6867):
    url = 'https://rejestr.io/krs/' + str(krs_num)
    driver_organizations.get(url)

    if driver_organizations.title != 'Nie znaleziono strony | Rejestr.io':
        organization_name = driver_organizations.find_element(By.XPATH, '//div[@class="h1_wrapper"]/h1/a').text
        #krs_dataset.loc[len(krs_dataset.index)] = [organization_name]

        link_to_representatives = driver_organizations.find_element(By.LINK_TEXT, 'Powiązania').get_attribute("href")
        driver_representatives.get(link_to_representatives)
        print(organization_name)
        representatives = driver_representatives.find_elements(By.CSS_SELECTOR, "div[class='media object person']")
        for representative in representatives:
            print('------' + representative.text)
            try:
                link_to_connections = driver_representatives.find_element(By.LINK_TEXT, representative.text).get_attribute("href")
                # print('------' + link_to_connections)
                driver_connections.get(link_to_connections)
                connections = driver_connections.find_elements(By.CSS_SELECTOR, "div[class='media object krs org']")
                for connection in connections:

                    # element_1 = connection.find_element(By.TAG_NAME, 'div')
                    # element_2 = element_1.find_element(By.TAG_NAME, 'p')
                    # new_connection_name = element_2.find_element(By.TAG_NAME, 'a').text
                    if connection.text != organization_name:
                        print('------------------' + connection.text)
                    else:
                        if len(connections) == 1:
                            print('------------------' + 'NaN')
            except Exception as e:
                print('------------------' + 'NaN')


driver_organizations.quit()
driver_representatives.quit()
driver_connections.quit()
# krs_dataset.to_csv('krs_data.csv', encoding='utf-8-sig', index=False)


