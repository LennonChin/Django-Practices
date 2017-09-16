# _*_ encoding: utf-8 _*_

from django.shortcuts import render

from django.views.generic import View

from .models import CourseOrg, CityDict, Teacher

from .forms import UserAskForm

from operation.models import UserFavorite

from courses.models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.http import HttpResponse
import json

# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_cities = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get('category', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # sort
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "course":
                all_orgs = all_orgs.order_by("-course_nums")

        # count
        org_nums = all_orgs.count()

        # pagination for orgs
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        paginator = Paginator(all_orgs, 5, request=request)
        orgs = paginator.page(page)

        context = {
            'all_orgs': orgs,
            'org_nums': org_nums,
            'all_cities': all_cities,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            "sort": sort
        }
        return render(request, 'org-list.html', context)


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg': 'error'}", content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            has_fav = True

        all_courses = course_org.course_set.all()
        all_teachers = course_org.teacher_set.all()
        context = {
            'current_page': current_page,
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-homepage.html', context)


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            has_fav = True

        all_courses = course_org.course_set.all()
        context = {
            'current_page': current_page,
            'course_org': course_org,
            'all_courses': all_courses,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            has_fav = True

        context = {
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            has_fav = True

        all_teachers = course_org.teacher_set.all()
        context = {
            'current_page': current_page,
            'course_org': course_org,
            'all_teachers': all_teachers,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-teachers.html', context)


class AddFavoriteView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '0')

        if not request.user.is_authenticated():
            return HttpResponse(json.dumps("{'status': 'fail', 'msg': 'not login'}"), content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            exist_records.delete()
            return HttpResponse(json.dumps("{'status': 'success', 'msg': 'cancel fav'}"), content_type='application/json')
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps("{'status': 'success', 'msg': 'fav success'}"), content_type='application/json')
            else:
                return HttpResponse(json.dumps("{'status': 'fail', 'msg': 'fav error'}"), content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # sort
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        # pagination for orgs
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        paginator = Paginator(all_teachers, 1, request=request)
        all_teachers = paginator.page(page)

        context = {
            'all_teachers': all_teachers,
            'sorted_teachers': sorted_teachers,
            'sort': sort
        }
        return render(request, 'teachers-list.html', context)

    def post(self, request):
        pass


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)

        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        context = {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teachers': sorted_teachers
        }
        return render(request, 'teacher-detail.html', context)