import numpy as np
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv


def initialize_driver() -> tuple:
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs', {
    'profile.managed_default_content_settings.images':2,
    'profile.default_content_setting_values.notifications':2,
    'profile.managed_default_content_settings.stylesheets':2,
    'profile.managed_default_content_settings.cookies':2,
    'profile.managed_default_content_settings.javascript':1,
    'profile.managed_default_content_settings.geolocation':2,
    'profile.managed_default_content_settings.media_stream':2,
    })
    options.add_argument("--headless=new")

    driver_org = webdriver.Chrome(options=options)
    driver_rep = webdriver.Chrome(options=options)
    driver_con = webdriver.Chrome(options=options)
    return driver_org, driver_rep, driver_con


def scrape_krs_data(start_num: int, end_num: int) -> pd.DataFrame:
    driver_organizations, driver_representatives, driver_connections = initialize_driver()
    krs_dataset = pd.DataFrame(columns=['OrganizationName', 'Representatives', 'ConnectedOrganizations'])

    for krs_num in range(start_num, end_num):
        print(f'KRS Counter: {krs_num}')

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
    return krs_dataset


if __name__ == '__main__':
    start_num = 20000
    end_num = 25000
    krs_dataset = scrape_krs_data(start_num, end_num)
    krs_dataset.to_csv(f'krs_data_{start_num}_{end_num}.csv', encoding='utf-8-sig', index=False, sep=',', quotechar='"',
                       quoting=csv.QUOTE_ALL)