# ВАКАНСИИ
import requests
import pprint

DOMAIN = 'https://api.hh.ru/'


def area_choice():
    while True:
        area_answer = input('Введите название региона для поиска (по умолчанию Москва): ')
        url_area = f'{DOMAIN}suggests/areas'
        params = {'text': f'{area_answer}'}
        print('Проверяем ...')
        r = requests.get(url_area, params=params)
        if r.status_code == 200:
            result = r.json()
            if result['items']:
                print(f'Ищем вакансию в регионе {area_answer}')
                return result['items'][0]['id']
            else:
                print('Такого региона нет!')
        else:
            print('Ищем вакансию по умолчанию в Москве')
            break

    return '1'


if __name__ == '__main__':
    area_param = area_choice()  # выбираем регион, по умолчанию Москва
    ############
    vacancy_answer = input('Введите название вакансии для поиска (по умолчанию python developer):')
    vacancy_answer = 'python developer'
    url_vacancies = f'{DOMAIN}vacancies'
    par = {'text': vacancy_answer, 'area': area_param}
    r = requests.get(url_vacancies, params=par)
    result = r.json()
    # print(result['found'])
    pprint.pprint(result)
    # items = result['items']
    # first = items[0]
    # print(first['area'])
