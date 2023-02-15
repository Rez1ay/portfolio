from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

url = 'https://www.fleetmon.com/businesses/'
driver = webdriver.Chrome()
driver.maximize_window()

def main():

    make_table()

    try:
        driver.get(url=url)
        driver.implicitly_wait(5)
        action = ActionChains(driver)

        authorization()
        driver.implicitly_wait(5)

        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div/a').click()
        except Exception:
            pass

        while True:
            time.sleep(3)
            companies = driver.find_element(By.XPATH, '//*[@id="businessregister_table"]/tbody').find_elements(By.CLASS_NAME, 'name')

            home = driver.window_handles[0]

            for company in companies:
                company = WebDriverWait(company, 5).until(EC.element_to_be_clickable((By.TAG_NAME, 'a')))

                action.key_down(Keys.CONTROL).click(company).key_up(Keys.CONTROL).perform()

                driver.switch_to.window(driver.window_handles[1])

                data = {
                    'Street': 'No data', 'City': 'No data', 'Country': 'No data', 'Mail': 'No data', 'Phone': 'No data',
                    'Fax': 'No data', 'Website': 'No data', '24h': 'No data'
                }

                try:
                    name = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/h1').text
                except Exception:
                    name = 'No data'

                try:
                    category = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/span').text
                except Exception:
                    category = 'No data'

                info = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]').find_elements(By.TAG_NAME, 'li')
                for i in info:
                    data[i.text.split(' ')[0]] = ' '.join(i.text.split(' ')[1:])
                    try:
                        del data['ZIP']
                    except Exception:
                        pass

                if len(driver.find_element(By.XPATH, '//*[@id="content"]/div[1]').find_elements(By.TAG_NAME, 'div')) > 2:
                    info = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]').find_elements(By.TAG_NAME, 'li')
                    for i in info:
                        data[i.text.split(' ')[0]] = ' '.join(i.text.split(' ')[2:])
                        try:
                            del data['Busin.']
                        except Exception:
                            pass
                else: data['24h'] = 'No data'

                try:
                    ports = [port.text for port in driver.find_element(By.XPATH, '//*[@class="row"]/div/div').find_elements(By.TAG_NAME, 'a')]
                    ports = ', \n'.join(ports)
                except Exception:
                    ports = 'No data'

                profile = driver.find_element(By.XPATH, '//p').text.strip()
                if profile == "In case of missing or wrong data, or if you suspect copyright problems or misuse, please don't hesitate to inform us.":
                    profile = 'No data'

                with open('FleetMon_Parser.csv', 'a', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow(
                        (
                            name,
                            category,
                            data['Street'],
                            data['City'],
                            data['Country'],
                            data['Mail'],
                            '"'+data['Phone']+'"',
                            '"'+data['Fax']+'"',
                            data['Website'],
                            '"'+data['24h']+'"',
                            ports,
                            profile
                        )
                    )

                driver.close()
                driver.switch_to.window(home)
            try:
                driver.find_element(By.XPATH, '//*[@id="businessregister_table_next"]/a').click()
                driver.implicitly_wait(5)
            except Exception:
                print('Finish parsing')
                break

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def authorization():

    try:
        driver.find_element(By.XPATH, '//*[@id="fleetmon-main-nav"]/div[3]/ul/li/a').click()
    except Exception:
        driver.find_element(By.XPATH, '//*[@id="fleetmon-main-nav"]/div[3]/div[2]').click()

    driver.implicitly_wait(5)

    driver.find_element(By.XPATH, '//*[@id="id_username"]').send_keys('USERNAME')   # input username
    driver.find_element(By.XPATH, '//*[@id="id_password"]').send_keys('PASSWORD')   # input password
    driver.find_element(By.XPATH, '//*[@id="button-sign-in"]').click()

def make_table():

    with open('FleetMon_Parser.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                'Company Name',
                'Category',
                'Address',
                'City',
                'Country',
                'email',
                'phone',
                'fax',
                'web',
                'phone24',
                'Ports',
                'Company profile'
            )
        )

if __name__ == '__main__':
    main()