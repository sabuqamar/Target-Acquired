from django.conf.urls import url
from .views import *
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
# Portal - continue as student or login
    path('',
    auth_views.LoginView.as_view(template_name="staff/login.html"),
    name='portal'),
# About us
    path('about_us',
    AboutUsView,
    name='about'),


# redirect to correct lab
    path('lab',
    redirectLabView,
    name='select_lab'),
# if TA
# Select a lab
    path('staff/lab',
    selectLabSessionTAView,
    name='select_lab_ta'),
# Select a person
    url('staff/select/(?P<topic_filter>-?\d+)/',
    SelectStudentView,
    name='select_student_filtered'),
    url('staff/select/',
    SelectStudentView,
    name='select_student'),
# Service request
    path('staff/service',
    ServiceRequestView,
    name='service_request'),
# logout
    path('staff/logout',
    LogoutView,
    name='logout'),
# logout successful - redirect to portal
    path('staff/logout_success',
    LogoutSuccessView,
    name='logout_success'),

# if lecturer
# stats page
    path('staff/statistics',
    StatisticsView,
    name='stats'),

# if student
# not accessible by mobile - or please manually type your pc number!
    path('student/',
    errorMobileView,
    name='error_mobile'),
# select a lab
    path('student/select',
    selectLabSessionSTUDENTView,
    name='select_lab_student'),
# question or mark
    path('student/help',
    SelectQuestionOrMarkView,
    name='question_or_mark'),
# question or mark
    path('student/question',
    AskQuestionView,
    name='ask_question'),
# waiting page
    path('student/waiting',
    WaitView,
    name='waiting'),

# administrator/demo pages
# demo dashboard
    path('demo/',
    DemoDashView,
    name='demo_home'),
# clear all users and data
    path('demo/drop',
    ClearDBView,
    name='drop'),
# setup demo data
    path('demo/setup',
    SetupDBView,
    name='setup'),
# add new user
    path('demo/new/user',
    NewUserView,
    name='new_user'),
# add new topic
    path('demo/new/topic',
    NewTopicView,
    name='new_topic'),
# add new lab session
    path('demo/new/lab_session',
    NewLabSessionView,
    name='new_lab'),
]