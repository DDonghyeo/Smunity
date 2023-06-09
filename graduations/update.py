# 장고 환경
import os
import json
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

from accounts.models import Department, Year
from graduations.models import Subject, Major, Culture
from config.settings import SUBTYPE_CHOICES_S, SUBTYPE_CHOICES_E


# 과목 업데이트 스크립트
def subjects(year, semester):
    print(f'{year}-{semester}')
    file_path = f'dataset/{year}_{semester}.json'
    with open(file_path, 'r') as f:
        datas = json.load(f)['dsUcsLectLsnPdoc']
        for data in datas:
            SBJ_NO = data['SBJ_NO']
            if not Subject.objects.filter(number=SBJ_NO):
                Subject.objects.create(number=SBJ_NO, name=data['SBJ_NM'], credit=data['CDT'], dept=data['EST_DEPT_INFO'], type=data['CMP_DIV_NM'])


# 전공 과목 업데이트 스크립트
def major(dept, subjects):
    for subject in subjects:
        numbers = subject['numbers']
        for number in numbers:
            try:
                sub = Subject.objects.get(number=number)
                Major.objects.create(department=dept, subject=sub, grade=subject['grade'], semester=subject['semester'], type=subject['type'])
            except:
                print(number)


# 학년도 업데이트 스크립트
def year():
    datas = [
        {'year': '2017', 'major_i': 15, 'major_s': 45, 'culture': 36, 'culture_cnt': 4, 'all': 130},
        {'year': '2018', 'major_i': 15, 'major_s': 45, 'culture': 33, 'culture_cnt': 4, 'all': 130},
        {'year': '2019', 'major_i': 15, 'major_s': 45, 'culture': 33, 'culture_cnt': 4, 'all': 130},
        {'year': '2020', 'major_i': 15, 'major_s': 45, 'culture': 33, 'culture_cnt': 5, 'all': 130},
        {'year': '2021', 'major_i': 15, 'major_s': 45, 'culture': 33, 'culture_cnt': 5, 'all': 130},
        {'year': '2022', 'major_i': 15, 'major_s': 45, 'culture': 33, 'culture_cnt': 5, 'all': 130},
        {'year': '2023', 'major_i': 15, 'major_s': 60, 'culture': 33, 'culture_cnt': 5, 'all': 130}
    ]
    for data in datas:
        Year.objects.create(year=data['year'], major_i=data['major_i'], major_s=data['major_s'], culture=data['culture'], culture_cnt=data['culture_cnt'], all=data['all'])


# 학과 업데이트 스크립트
def departments():
    datas = [
        {'college': '융합공과대학', 'name': '컴퓨터과학전공', 'type': '공학', 'call': '02-2287-5292'}
    ]
    for data in datas:
        Department.objects.create(college=data['college'], name=data['name'], type=data['type'], call=data['call'])


# 상명핵심역량교양 과목 업데이트 스크립트
def culture_e():
    dic = {
        '창의적문제해결역량': ['HALF7023', 'HALF9326', 'HALR1040', 'HALR1046', 'HALR1230'],
        '융복합역량': ['HALF9037', 'HALF9320', 'HALF9374', 'HALF9378', 'HALR1235'],
        '다양성존중역량': ['HALF0122', 'HALF9340', 'HALF9343', 'HALF9360', 'HALR1041'],
        '윤리실천역량': ['HALF9238', 'HALF9280', 'HALF9379', 'HALF9404', 'HALR1038']
    }
    types = list(map((lambda x: x[0]), SUBTYPE_CHOICES_E))
    for type in types:
        numbers = dic[type]
        for number in numbers:
            try:
                subject = Subject.objects.get(number=number)
                Culture.objects.create(subject=subject, type='교필', domain='핵심', subdomain=type)
            except:
                print(number)


# 균형교양 과목 업데이트 스크립트
def culture_s():
    dic = {
        '인문': ['HALF0102', 'HALF0202', 'HALF0302', 'HALF9013', 'HALF9014', 'HALF9015', 'HALF9302', 'HALF9305', 'HALF9338', 'HALF9358'],
        '사회': ['HALF0447', 'HALF4033', 'HALF5013', 'HALF9030', 'HALF9031', 'HALF9245', 'HALF9266'], # HALF9421
        '자연': ['HALF0502', 'HALF0537', 'HALF9041', 'HALF9239', 'HALF9252', 'HALF9321', 'HALF9362', 'HALF9403'],
        '공학': ['HALF6024', 'HALF9319', 'HALF9329', 'HALF9405', 'HALF9420'],
        '예술': ['HALF0601', 'HALF0628', 'HALF6071', 'HALF6072', 'HALF9061', 'HALF9356']
    }
    types = list(map((lambda x: x[0]), SUBTYPE_CHOICES_S))
    for type in types:
        numbers = dic[type]
        for number in numbers:
            try:
                subject = Subject.objects.get(number=number)
                Culture.objects.create(subject=subject, type='교선', domain='균형', subdomain=type)
            except:
                print(number)


# 컴퓨터과학과 전공 업데이트 스크립트
def major_computer_science():
    dept = Department.objects.get(name='컴퓨터과학전공')
    subjects = [
        {'grade': '1학년', 'semester': '1학기', 'type': '1전선', 'numbers': ['HASW0001', 'HAEA9225', 'HAEA9237', 'HAFL7001']},
        {'grade': '1학년', 'semester': '2학기', 'type': '1전선', 'numbers': ['HASW0002', 'HAEA0032', 'HAEA9226', 'HAFL0012']},
        {'grade': '2학년', 'semester': '1학기', 'type': '1전선',
         'numbers': ['HAEA0001', 'HAEA0017', 'HAEA0027', 'HAEA9236', 'HAEA9241', 'HAFL0002']},
        {'grade': '2학년', 'semester': '2학기', 'type': '1전선',
         'numbers': ['HAEA0002', 'HAEA0003', 'HAEA0010', 'HAEA9227', 'HAEZ0002', 'HAEZ0004']},
        {'grade': '3학년', 'semester': '1학기', 'type': '1전선', 'numbers': ['HAEA0005', 'HAEA9239', 'HAEA9243']},
        {'grade': '3학년', 'semester': '1학기', 'type': '1전심', 'numbers': ['HAEA0004', 'HAEA0008', 'HAEA0012', 'HAEZ0003']},
        {'grade': '3학년', 'semester': '2학기', 'type': '1전선', 'numbers': ['HAEA0013', 'HAEA9002', 'HAEA9213']},    # HAEA9244
        {'grade': '3학년', 'semester': '2학기', 'type': '1전심', 'numbers': ['HAEA0011', 'HAEA0014', 'HAEA9228', 'HAGH0030']},
        {'grade': '4학년', 'semester': '1학기', 'type': '1전선', 'numbers': ['HAEA0020', 'HAEA9229', 'HAEA9240']},
        {'grade': '4학년', 'semester': '2학기', 'type': '1전선', 'numbers': ['HAEA0026', 'HAEA9231']},
    ]
    major(dept, subjects)


# 전체 업데이트 스크립트 (17학년도 ~ 22학년도)
def subjects_all():
    data = [['2017', '10'], ['2017', '11'], ['2017', '20'], ['2017', '21'], ['2018', '10'], ['2018', '11'],
            ['2018', '20'], ['2018', '21'], ['2019', '10'], ['2019', '11'], ['2019', '20'], ['2019', '21'],
            ['2020', '10'], ['2020', '11'], ['2020', '20'], ['2020', '21'], ['2021', '10'], ['2021', '11'],
            ['2021', '20'], ['2021', '21'], ['2022', '10'], ['2022', '11'], ['2022', '20'], ['2022', '21'], ['2023', '10']]
    for d in data:
        subjects(d[0], d[1])


if __name__ == '__main__':
    subjects_all()
    year()
    departments()
    major_computer_science()
    culture_e()
    culture_s()
