from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Q
from config.settings import YEAR_CHOICES, DEPARTMENT_CHOICES, SUBTYPE_CHOICES_S, COLLEGE_CHOICES


class Year(models.Model):   # 학년도 테이블
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)     # 학번
    major_i = models.IntegerField()         # 전심
    major_s = models.IntegerField()         # 전선
    culture = models.IntegerField()         # 교양 전체
    culture_cnt = models.IntegerField()     # 기초교양 개수
    all = models.IntegerField()             # 전체

    def __str__(self):
        return self.year


class Department(models.Model):     # 학과 테이블
    college = models.CharField(max_length=20, choices=COLLEGE_CHOICES)  # 소속 단과대
    name = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)  # 학과 이름
    type = models.CharField(max_length=2, choices=SUBTYPE_CHOICES_S)    # 균교 타입
    call = models.CharField(max_length=20, null=True, blank=True)       # 학과 사무실 전화번호
    def __str__(self):
        return f'[{self.college}] {self.name}'


class Profile(models.Model):    # 사용자 프로필
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    # 장고 유저
    year = models.ForeignKey(Year, on_delete=models.CASCADE)                # 학번
    department = models.ForeignKey(Department, on_delete=models.CASCADE)    # 학과
    name = models.CharField(max_length=10)  # 본명

    def __str__(self):
        return f'[{self.year}] {self.user} {self.name} - {self.department}'

    def subjects_all(self):
        from core.models import Course
        return Course.objects.filter(user=self.user).aggregate(Sum('credit'))['credit__sum']

    def subjects_major_i(self):
        from core.models import Course
        return Course.objects.filter(user=self.user, type='1전심').aggregate(Sum('credit'))['credit__sum']

    def subjects_major_s(self):
        from core.models import Course
        return Course.objects.filter(user=self.user, type='1전선').aggregate(Sum('credit'))['credit__sum']

    def subjects_culture(self):
        from core.models import Course
        return Course.objects.filter(user=self.user, type__in=['교필', '교선']).aggregate(Sum('credit'))['credit__sum']

    def subjects_culture_e(self):
        from core.models import Course
        from graduations.models import Culture
        culture_e1 = Course.objects.filter(Q(user=self.user)&(Q(domain__contains='창의적문제해결역량')|Q(domain__contains='융복합역량')))
        culture_e2 = Course.objects.filter(Q(user=self.user)&(Q(domain__contains='다양성존중역량')|Q(domain__contains='윤리실천역량')))
        subject_e1 = Culture.objects.filter(Q(subdomain__contains='창의적문제해결역량')|Q(subdomain__contains='융복합역량'))
        subject_e2 = Culture.objects.filter(Q(subdomain__contains='다양성존중역량')|Q(subdomain__contains='윤리실천역량'))
        cnt = 0
        if culture_e1:
            cnt += 1
        if culture_e2:
            cnt += 1
        context = {'cnt': cnt, 'culture_e1': culture_e1, 'culture_e2': culture_e2, 'subject_e1': subject_e1, 'subject_e2': subject_e2}
        return context

    def subjects_culture_s(self):
        from core.models import Course
        cnt = 0
        cultures, subs = [], []
        types = list(map((lambda x: x[0]), SUBTYPE_CHOICES_S))
        types.remove(self.department.type)

        for type in types:
            subjects = Course.objects.filter(Q(user=self.user)&Q(domain__contains=type)&Q(domain__contains='균형'))
            cultures.append({'type': type, 'subjects': subjects})
            if subjects:
                cnt += 1
            else:
                from graduations.models import Culture
                subs.append({'type': type, 'cultures': Culture.objects.filter(subdomain=type)})
        context = {'cnt': cnt, 'cultures': cultures, 'subjects': subs}
        return context
