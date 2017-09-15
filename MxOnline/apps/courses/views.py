# _*_ encoding: utf-8 _*_

from django.shortcuts import render

from django.views.generic import View

from django.http import HttpResponse

from .models import Course, Video

from users.models import UserProfile

from operation.models import UserFavorite, CourseComments, UserCourse

from courses.models import CourseResource

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from utils.mixin_utils import LoginRequireMixin

import json

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # sort
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # pagination for all_courses
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        paginator = Paginator(all_courses, 3, request=request)
        courses = paginator.page(page)

        context = {
            'courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        }
        return render(request, 'course-list.html', context)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:2]
        else:
            relate_course = []
        context = {
            'course': course,
            'relate_course': relate_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        }

        tag = course.tag

        return render(request, 'course-detail.html', context)


class CourseInfoView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)

        # 取出学过该课程所有用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出所有用户对应的UserCourse对象；django查询in的一种特定的写法
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有的课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程的用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses

        }
        return render(request, 'course-video.html', context)


class CourseCommentView(LoginRequireMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        context = {
            'course': course,
            'all_comments': all_resources,
            'all_comments': all_comments
        }
        return render(request, 'course-comment.html', context)

    def post(self, request):
        pass


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps("{'status': 'fail', 'msg': 'not login'}"), content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comments', '')

        if course_id > 0 and comment:
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse(json.dumps("{'status': 'success', 'msg': 'add success'}"), content_type='application/json')
        else:
            return HttpResponse(json.dumps("{'status': 'fail', 'msg': 'add fail'}"), content_type='application/json')


class VideoPlayView(View):
    def get(self, request, course_id):
        video = Video.objects.get(id=int(course_id))
        course = video.lesson.course
        course.students += 1
        course.save()
        # 查询用是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)

        # 取出学过该课程所有用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出所有用户对应的UserCourse对象；django查询in的一种特定的写法
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有的课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程的用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        context = {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video
        }
        return render(request, 'course-play.html', context)