import numpy as np
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import csv


def initialize_driver() -> tuple:
    options = webdriver.ChromeOptions()
    driver_org = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver_rep = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver_con = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver_org, driver_rep, driver_con


def scrape_krs_data(start_num: int, end_num: int) -> pd.DataFrame:
    driver_organizations, driver_representatives, driver_connections = initialize_driver()
    krs_dataset = pd.DataFrame(columns=['KRS', 'OrganizationName', 'LegalForm', 'Representatives', 'RepresentativesID',
                                        'ConnectedOrganizations'])

    for krs_num in range(start_num, end_num):
        print(f'KRS: {krs_num}')
        url = 'https://rejestr.io/krs/' + str(krs_num)
        driver_organizations.get(url)

        if driver_organizations.title != 'Nie znaleziono strony | Rejestr.io':
            try:
                organization_name = driver_organizations.find_element(By.XPATH, '//div[@class="h1_wrapper"]/h1/a').text
            except NoSuchElementException:
                organization_name = np.nan

            try:
                legal_form = driver_organizations.find_element(By.CSS_SELECTOR,
                                                               "div[data-name='forma_prawna'] .val.text-normalize span").text
            except NoSuchElementException:
                legal_form = np.nan

            try:
                link_to_representatives = driver_organizations.find_element(By.LINK_TEXT, 'Powiązania').get_attribute(
                    "href")
            except NoSuchElementException:
                link_to_representatives = None

            if link_to_representatives:
                driver_representatives.get(link_to_representatives)
                representatives = driver_representatives.find_elements(By.CSS_SELECTOR,
                                                                       "div[class='media object person']")
                representatives_id = driver_representatives.find_elements(By.CSS_SELECTOR, 'li[data-global-id]')
                list_of_representatives_id = []
                count = 0

                for id in representatives_id:
                    rep_id = id.get_attribute("data-global-id")
                    rep_id = ''.join(filter(str.isdigit, rep_id))
                    list_of_representatives_id.append(rep_id)

                for representative in representatives:
                    krs_dataset_row = dict.fromkeys(
                        ['KRS', 'OrganizationName', 'LegalForm', 'Representatives', 'RepresentativesID',
                         'ConnectedOrganizations'])
                    krs_dataset_row['KRS'] = krs_num
                    krs_dataset_row['LegalForm'] = legal_form
                    krs_dataset_row['OrganizationName'] = '"' + organization_name + '"'
                    krs_dataset_row['Representatives'] = representative.text
                    krs_dataset_row['RepresentativesID'] = list_of_representatives_id[count]

                    link_to_connections = None
                    try:
                        link_to_connections = driver_representatives.find_element(By.LINK_TEXT,
                                                                                  representative.text).get_attribute(
                            "href")
                    except NoSuchElementException:
                        pass

                    if link_to_connections:
                        list_of_connections = []
                        list_of_connections_krs = []
                        driver_connections.get(link_to_connections)
                        connections = driver_connections.find_elements(By.CSS_SELECTOR,
                                                                       "div[class='media object krs org']")
                        connections_krs = driver_connections.find_elements(By.CSS_SELECTOR, 'li[data-global-id]')

                        for connection_krs in connections_krs:
                            org_num = connection_krs.get_attribute("data-global-id")
                            org_num = ''.join(filter(str.isdigit, org_num))
                            if int(org_num) != krs_num:
                                list_of_connections_krs.append(org_num)

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
                        krs_dataset_row['ConnectedOrganizations'] = str(
                            dict(zip(list_of_connections, list_of_connections_krs))).replace('{', '').replace('}',
                                                                                                              '')
                    else:
                        krs_dataset_row['ConnectedOrganizations'] = np.nan

                    krs_dataset = pd.concat([krs_dataset, pd.DataFrame([krs_dataset_row])], ignore_index=True)
                    count += 1

    driver_organizations.quit()
    driver_representatives.quit()
    driver_connections.quit()
    return krs_dataset


if __name__ == '__main__':
    start_num = 20000
    end_num = 20100
    krs_dataset = scrape_krs_data(start_num, end_num)
    krs_dataset.to_csv(f'data/krs_data_{start_num}_{end_num}.csv', encoding='utf-8-sig', index=False, sep=',',
                       quotechar='"', quoting=csv.QUOTE_ALL)
