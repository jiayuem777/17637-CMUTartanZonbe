from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('',views.home,name='default'),
    path('all_courses/',views.all_courses,name='all_courses'),
    path('course_review/<int:course_id>',views.course_review,name='course_review'),

    #admin
    path('add_course/',views.add_course,name='add_course'),
    #admin
    path('edit_course/<int:course_id>',views.edit_course,name='edit_course'),
    #admin
    path('update_course/<int:course_id>',views.update_course,name='update_course'),
    #admin
    path('delete_course/<int:course_id>',views.delete_course,name='delete_course'),
    path('my_group/', views.my_group, name='my_group'),
    path('group_disccusion/<int:group_id>/<int:post_id>', views.group_discussion, name='group_discussion'),
    path('group_disccusion/<int:group_id>', views.group_discussion1, name='group_discussion1'),
    path('new_post/<int:group_id>', views.new_post, name='new_post'),
    path('reply_postanswer/<int:group_id>/<int:post_id>/<int:answer_id>', views.reply_postanswer, name='reply_postanswer'),
    path('delete_postanswer/<int:group_id>/<int:post_id>/<int:answer_id>', views.delete_postanswer, name='delete_postanswer'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('home/',views.home,name='home'),
    path('add_to_my_course/<int:course_id>',views.add_to_my_course,name='add_to_my_course'),
    path('leave_review/<int:course_id>',views.leave_review,name='leave_review'),
    path('logout/',views.logout,name='logout'),
    path('my_course/',views.my_course,name='my_course'),
    path('my_course_review/<int:course_id>',views.my_course_review,name='my_course_review'),
    path('drop_course/<int:course_id>',views.drop_course,name='drop_course'),
    path('instructor_profile/<int:instructor_id>',views.instructor_profile,name='instructor_profile'),
    path('all_instructor/',views.all_instructor,name='all_instructor'),
    #admin
    path('add_instructor/',views.add_instructor,name='add_instructor'),
    #admin
    path('edit_instructor/<int:instructor_id>',views.edit_instructor,name='edit_instructor'),
    #admin
    path('delete_instructor/<int:instructor_id>',views.delete_instructor,name='delete_instructor'),
    #admin
    path('delete_review/<int:review_id>/<int:course_id>',views.delete_review,name='delete_review'),
    path('join_group/<int:course_id>',views.join_group,name='join_group'),
    #admin
    path('create_group/',views.create_group,name='create_group'),
    #admin
    path('create_group_1/',views.create_group_1,name='create_group_1'),
    path('delete_member/<mname>',views.delete_member,name='delete_member'),
    #admin
    path('manage_group/',views.manage_group,name='manage_group'),
    #admin
    path('delete_group/',views.delete_group,name='delete_group'),
    path('quit_group/<gname>',views.quit_group,name='quit_group'),
    path('search_course',views.search_course,name='search_course'),
    path('search_instructor', views.search_instructor,name='search_instructor'),
    path('ajax_agree',views.ajax_agree,name='ajax_agree'),
    path('ajax_disagree',views.ajax_disagree,name='ajax_disagree'),
    path('scheduel',views.scheduel,name='scheduel'),
    path('edit_post/<int:post_id>/<int:group_id>',views.edit_post,name='edit_post'),
    path('all_reviews/<int:course_id>',views.all_reviews,name='all_reviews'),
    #admin
    path('add_schedule/<int:course_id>',views.add_schedule,name='add_schedule'),
    #admin
    path('add_admin/',views.add_admin,name="add_admin"),
    #admin
    path('ajax_add_course/',views.ajax_add_course,name='ajax_add_course'),
    #admin
    path('ajax_add_instructor/',views.ajax_add_instructor,name='ajax_add_instructor'),
    #admin
    path('ajax_add_schedule/', views.ajax_add_schedule, name='ajax_add_schedule'),

]
