import requests
from bs4 import BeautifulSoup
import csv

def main():

    with open('Parser_Seavendors.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                'Company Name',
                'Specialized In',
                'Address',
                *['Phone1', 'Phone2', 'Phone3', 'Phone4', 'Phone5'],
                'Email',
                'Web',
                'FB',
                'LinkedIn'
            )
        )

    page = 1
    while True:
        url = f'https://seavendors.com/cat/ship-spares-stores/page/{page}/?count=20&orderby=title&order=ASC'

        req = requests.get(url)
        src = req.text

        soup = BeautifulSoup(src, 'lxml')

        error_try = soup.find(class_='error404')
        if error_try != None:
            break

        print(f'Обработка странцы номер {page}')

        companies = soup.find_all('div', class_='item-title')

        for company in companies:
            url_comp = company.find('a').get('href')

            req = requests.get(url_comp)
            src = req.text

            soup = BeautifulSoup(src, 'lxml')

            try:
                company_name = soup.find(class_='entry-title-wrap').find('h1').text
            except Exception:
                company_name = 'No data'

            try:
                specialized_list = soup.find(class_='entry-title-wrap').find(class_='breadcrumbs').find_all('a')
                specialized_in = [i.text for i in specialized_list[2:]]
                specialized_in = ', \n'.join(specialized_in)
            except Exception:
                specialized_in = 'No data'

            contacts = soup.find(class_='address-container').find(class_='content')

            try:
                address = contacts.find(class_='row-postal-address').find(class_='address-data').text
            except Exception:
                address = 'No data'

            try:
                phones = contacts.find(class_='row-telephone').find(class_='address-data').find_all(class_='phone')
                phone_list = [i.text.strip() for i in phones]
            except Exception:
                phone_list = []

            phone_dict = {}
            for i in range(1, 6):
                try:
                    phone_dict['phone' + str(i)] = '"'+phone_list[i-1]+'"'
                except IndexError:
                    phone_dict['phone' + str(i)] = 'No data'

            try:
                email = contacts.find(class_='row-email').find(class_='address-data').find('p').text
            except Exception:
                email = 'No data'

            if email == '-':
                email = 'No data'

            try:
                web = contacts.find(class_='row-web').find(class_='address-data').find('p').text.replace(' ', '')
            except Exception:
                web = 'No data'

            if web == '-':
                web = 'No data'

            FB, LinkedIn = 0, 0
            try:
                social_list = contacts.find(class_='row-social').find(class_='content').find_all('li')
                for social in social_list:

                    if 'www.facebook.com' in social.find('a').get('href'):
                        FB = social.find('a').get('href')
                    elif 'www.linkedin.com' in social.find('a').get('href'):
                        LinkedIn = social.find('a').get('href')
            except Exception:
                pass

            if FB == 0:
                FB = 'No data'

            if LinkedIn == 0:
                LinkedIn = 'No data'

            with open('Parser_Seavendors.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(
                    (
                        company_name,
                        specialized_in,
                        address,
                        *phone_dict.values(),
                        email,
                        web,
                        FB,
                        LinkedIn
                    )
                )

        page += 1

if __name__ == '__main__':
    main()