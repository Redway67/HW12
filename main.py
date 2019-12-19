# ВАКАНСИИ
import requests
import pprint
import time
import json

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
    total = 0
    qnt_skills = 0
    print('Ищем:')

    for p in range(1 + (found // 20)):
        params = {'text': vacancy_answer, 'area': area_param[0], 'page': p}
        results = requests.get(url_vacancies, params=params).json()
        print(f' Страница {p}')

        for j in results['items']:
            print(' ', end='.')
            resultj = requests.get(j['url']).json()
            for i in resultj['key_skills']:
                if i['name'] in skills:
                    skills[i['name']] += 1
                else:
                    skills.setdefault(i['name'], 1)
                    qnt_skills += 1
                total += 1
        print('\n')

    print('Статистика:')
    req = []
    for k, v in sorted(skills.items(), key=lambda x: int(x[1]), reverse=True):
        print(round(v / total * 100, 2), '%   ', k, ':', v)
        skill = {'name': k, 'count': v, 'percent': round(v / total * 100, 2)}  # в формате как в задании
        req.append(skill)
    print(f'Всего {qnt_skills} навыков')
    return req


if __name__ == '__main__':
    area_param = area_choice()  # выбираем регион, по умолчанию Москва

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

            requirements = get_statistic()  # считаем статистику
            info = {'keywords': vacancy_answer, 'count': found, 'requirements': requirements}  # в формате как в задании
            file_name = (vacancy_answer.title()+'_'+area_param[1]).replace(' ', '')
            with open(file_name+'.json', 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False)

        else:
            print(f'В регионе {area_param[1]} вакансии {vacancy_answer} не найдено.')
    else:
        print('Ошибка поиска!')
