# ВАКАНСИИ
import requests
import pprint
import time

DOMAIN = 'https://api.hh.ru/'
FOUND_RESTRICTION_HH = 2000  # ограничение hh.ru на количество выводимых вакансий


def area_choice():
    # Возвращаем id, и название региона
    while True:
        area_answer = input('Введите название региона для поиска (по умолчанию Москва): ')
        url_area = f'{DOMAIN}suggests/areas'
        params = {'text': f'{area_answer}'}
        print('Проверяем есть ли такой регион...')
        ra = requests.get(url_area, params=params)
        if ra.status_code == 200:
            area_result = ra.json()
            if area_result['items']:
                print(f'Регион {area_answer} есть, ищем в нем')
                return [area_result['items'][0]['id'], area_answer]
            else:
                print('Такого региона нет!')
        else:
            print('Ищем вакансию по умолчанию в Москве')
            break

    return ['1', 'Москва']


def get_statistic():
    skills = {}
    for p in range(found//100+1):
        params = {'text': vacancy_answer, 'area': area_param[0], 'page': p}
        results = requests.get(url_vacancies, params=params).json()
        for j in results['items']:
            resultj = requests.get(j['url']).json()
            for i in resultj['key_skills']:
                if i['name'] in skills:
                    skills[i['name']] += 1
                else:
                    skills.setdefault(i['name'], 1)

    def by_value(item):
        return item[1]

    for k, v in sorted(skills.items(), key=by_value, reverse= True):
        print(k, '->', v)

    return


if __name__ == '__main__':
    area_param = area_choice()  # выбираем регион, по умолчанию Москва
    # здесь можно еще добавлять будущие параметры

    vacancy_answer = input('Введите название вакансии для поиска (по умолчанию python developer):')
    if not vacancy_answer:
        vacancy_answer = 'python developer'  # по умолчанию ищем python developer
    url_vacancies = f'{DOMAIN}vacancies'
    par = {'text': vacancy_answer, 'area': area_param[0]}  # добавляем параметры
    r = requests.get(url_vacancies, params=par)
    if r.status_code == 200:
        result = r.json()
        found = result['found']
        if result['items']:
            print(f'В регионе {area_param[1]} вакансия {vacancy_answer} найдено {found} раз.')
            if found > FOUND_RESTRICTION_HH:
                print(
                    f'Из-за ограничения на hh.ru статистика будет рассчитана по {FOUND_RESTRICTION_HH} вакансий!')
                found = FOUND_RESTRICTION_HH
            get_statistic()
        else:
            print(f'В регионе {area_param[1]} вакансии {vacancy_answer} не найдено.')
    else:
        print('Ошибка поиска!')
