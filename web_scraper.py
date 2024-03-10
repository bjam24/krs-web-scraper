import numpy as np
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv

krs_dataset = pd.DataFrame(columns=['OrganizationName', 'Representatives', 'ConnectedOrganizations'])

driver_organizations = webdriver.Chrome()
driver_representatives = webdriver.Chrome()
driver_connections = webdriver.Chrome()

for krs_num in range(6865, 7200):
    url = 'https://rejestr.io/krs/' + str(krs_num)
    driver_organizations.get(url)

    if driver_organizations.title != 'Nie znaleziono strony | Rejestr.io':
        organization_name = driver_organizations.find_element(By.XPATH, '//div[@class="h1_wrapper"]/h1/a').text

        link_to_representatives = driver_organizations.find_element(By.LINK_TEXT, 'Powiązania').get_attribute("href")
        driver_representatives.get(link_to_representatives)
        representatives = driver_representatives.find_elements(By.CSS_SELECTOR, "div[class='media object person']")

        for representative in representatives:
            krs_dataset_row = dict.fromkeys(['OrganizationName', 'Representatives', 'ConnectedOrganizations'])
            krs_dataset_row['OrganizationName'] = '"' + organization_name + '"'
            krs_dataset_row['Representatives'] = representative.text

            link_to_connections = None
            try:
                link_to_connections = driver_representatives.find_element(By.LINK_TEXT, representative.text).get_attribute("href")
            except NoSuchElementException:
                pass

            if link_to_connections:
                list_of_connections = []
                driver_connections.get(link_to_connections)
                connections = driver_connections.find_elements(By.CSS_SELECTOR, "div[class='media object krs org']")

                for connection in connections:
                    if "Obecnie: " in connection.text:
                        actual_connection_name = connection.text.split("Obecnie: ")[1].strip()
                        if len(connections) == 1 and actual_connection_name == organization_name:
                            krs_dataset_row['ConnectedOrganizations'] = np.nan
                        elif len(connections) > 1 and actual_connection_name == organization_name:
                            continue
                        elif len(connections) > 1 and actual_connection_name != organization_name:
                            list_of_connections.append(actual_connection_name)
                    else:
                        if len(connections) == 1 and connection.text == organization_name:
                            krs_dataset_row['ConnectedOrganizations'] = np.nan
                        elif len(connections) > 1 and connection.text == organization_name:
                            continue
                        elif len(connections) > 1 and connection.text != organization_name:
                            list_of_connections.append(connection.text)
                krs_dataset_row['ConnectedOrganizations'] = ', '.join(map(lambda x: f"'{x}'", list_of_connections))
            else:
                krs_dataset_row['ConnectedOrganizations'] = np.nan
            krs_dataset = pd.concat([krs_dataset, pd.DataFrame([krs_dataset_row])], ignore_index=True)

driver_organizations.quit()
driver_representatives.quit()
driver_connections.quit()

krs_dataset.to_csv('krs_data.csv', encoding='utf-8-sig', index=False, sep=',', quotechar='"', quoting=csv.QUOTE_ALL)
