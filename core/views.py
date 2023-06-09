import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from accounts.models import Profile
from config.settings import CULTURES_1, CULTURES_2, CULTURES_DIC1, CULTURES_DIC2, SUBTYPE_CHOICES_S
from core.models import Course
from graduations.models import Subject, Major


def home(request):
    return render(request, 'core/head.html')


@login_required
def mypage(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    courses = Course.objects.filter(user=user).order_by('-pk')
    return render(request, 'core/mypage.html', {'user': user, 'profile': profile, 'courses': courses})


@login_required
def custom(request):
    courses = Course.objects.filter(user=request.user, custom=False).order_by('-pk')
    customs = Course.objects.filter(user=request.user, custom=True).order_by('-pk')
    context = {'courses': courses, 'customs': customs}
    return render(request, 'core/custom.html', context)

@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user != course.user or not course.custom:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('core:custom')
    course.delete()
    return redirect('core:custom')

# 기이수과목 업로드
@login_required
def course_update(request):
    excel = request.FILES['excel']

    # 엑셀파일인지 검사
    if excel.name[-4:] != 'xlsx':
        messages.error(request, '⚠️ 잘못된 파일 형식입니다. 확장자가 xlsx인 파일을 올려주세요. ')
        return redirect('core:mypage')

    # 추가 전 기존 데이터 삭제
    courses = Course.objects.filter(user=request.user)
    if courses.exists():
        courses.delete()

    # 기이수과목 추가
    try:
        df = pd.read_excel(excel)
        for _, item in df.iterrows():
            if item[0].isnumeric():
                subject = Subject.objects.get(number=item[2])
                domain = item[19]
                if domain == '*':
                    domain = None
                Course.objects.create(user=request.user, subject=subject, year=item[0], semester=item[1], credit=item[7], type=item[6], domain=domain)
    except:
        messages.error(request, '⚠️ 엑셀 내용이 다릅니다! 수정하지 않은 엑셀파일을 올려주세요.')
        return redirect('core:mypage')
    messages.success(request, '업데이트성공')
    return redirect('core:mypage')

@login_required
def result(request):
    profile = get_object_or_404(Profile, user=request.user)
    courses = Course.objects.filter(user=request.user)

    culture_b = CULTURES_1
    culture_dic = CULTURES_DIC1
    if int(profile.year.year) > 2019:
        culture_b = CULTURES_2
        culture_dic = CULTURES_DIC2

    cnt = 0
    for culture, dics in zip(culture_b, culture_dic):
        q = Q()
        for key in dics:
            q |= Q(domain__contains=key)
        course = Course.objects.filter(q)
        culture['course'] = course
        if course:
            cnt += 1

    context = {
        'profile': profile, 'major_i': Major.objects.filter(department=profile.department, type='1전심').exclude(subject_id__in=courses.values_list('subject', flat=True)),
        'major_s': Major.objects.filter(department=profile.department, type='1전선').exclude(subject_id__in=courses.values_list('subject', flat=True)), 'culture_b': culture_b, 'culture_cnt': cnt,
        'subjects_all': profile.subjects_all(), 'subjects_major_i': profile.subjects_major_i(), 'subjects_major_s': profile.subjects_major_s(), 'subjects_culture': profile.subjects_culture,
        'subjects_culture_e': profile.subjects_culture_e(), 'subjects_culture_s': profile.subjects_culture_s()
    }
    return render(request, 'core/result.html', context)

def member_del(request):
    if request.method == "POST":
        pw_del = request.POST["pw_del"]
        user = request.user
        if check_password(pw_del, user.password):
            user.delete()
            return redirect('home')
    messages.error(request, '⚠️ 비밀번호가 일치하지 않습니다.')
    return redirect('core:mypage')
