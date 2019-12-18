from django.shortcuts import render,reverse,redirect
from .Forms import CourseForm, UserForm,InstructorForm, NewGroupForm, ScheduleForm
from .models import Course,TartanUser,Group,DiscussionPost,Review,Instructor, PostAnswer, PostAnswerReply, ReviewAgree, Temp, Schedule
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core import serializers
import random
from django.contrib import messages
from django.shortcuts import get_object_or_404



from django.contrib import messages



@csrf_exempt
def manage_group(request):
    user = get_object_or_404(TartanUser, user=request.user)
    if user.role=="administrator":
        groupobjs = Group.objects.all()
        course = Course.objects.all()
        gform = NewGroupForm()
        return render(request, 'tartanzone/manage_group.html', locals())
    else:
        return HttpResponse("you have no access to this page")

# Create your views here.
@csrf_exempt
def create_group(request):
    data= {}
    user1 = request.user
    tartanuser=get_object_or_404(TartanUser,user=user1)
    if tartanuser.role=='administrator':
        try:
            user = get_object_or_404(TartanUser, user=request.user)
        except:
            return render(request, 'tartanzone/manage_group.html', locals())
        try:
            course = Course.objects.all()
        except:
            return render(request, 'tartanzone/manage_group.html', locals())

        c = course
        groupobjs = Group.objects.all()
        if(request.method == "POST"):
            gform = NewGroupForm(request.POST)
            if gform.is_valid():
                tmp = gform.save(commit= False)
                tmp.group_owner = get_object_or_404(TartanUser, user = request.user)
                gform.save()
                try:
                    user = get_object_or_404(TartanUser, user=request.user)
                except:
                    return render(request, 'tartanzone/manage_group.html', locals())
                data['error'] = ""

                print("success")
            else:
                data['error'] = gform.errors
                print("error")
            return render(request, 'tartanzone/manage_group.html', locals())
        else:
            gform = NewGroupForm()
        return render(request, 'tartanzone/manage_group.html', locals())
    else:
        return HttpResponse("you have no access to this page")

@csrf_exempt
def create_group_1(request):
    data= {}
    user1 = request.user
    tartanuser=get_object_or_404(TartanUser,user=user1)
    if tartanuser.role=='administrator':
        try:
            user = TartanUser.objects.get(user=request.user)
        except:
            return render(request, 'tartanzone/manage_group.html', locals())
        try:
            course = Course.objects.all()
        except:
            return render(request, 'tartanzone/manage_group.html', locals())

        c = course
        groupobjs = Group.objects.all()
        if(request.method == "POST"):
            gform = NewGroupForm(request.POST)
            if gform.is_valid():
                tmp = gform.save(commit= False)
                tmp.group_owner = TartanUser.objects.get(user = request.user)
                gform.save()
                try:
                    user = TartanUser.objects.get(user=request.user)
                except:
                    return render(request, 'tartanzone/manage_group.html', locals())
                data['error'] = ""

                print("success")
            else:
                data['error'] = gform.errors
                print("error")
            return JsonResponse(data, safe=False)
        else:
            gform = NewGroupForm()
        return render(request, 'tartanzone/manage_group.html', locals())
    else:
        return HttpResponse("you have no access to this page")


@csrf_exempt
def delete_member(request, mname):
    user1 = request.user
    tartanuser=get_object_or_404(TartanUser,user=user1)
    if tartanuser.role=='administrator':
        if (request.method == "POST"):
            gname = request.POST.get("groupname")
            try:
                g = get_object_or_404(Group, name = gname)
            except:
                return render(request,'tartanzone/manage_group.html',locals())
            m = g.member
            mname = mname
            try:
                mobj = get_object_or_404(TartanUser, user = User.objects.get(username = mname))
            except:
                return render(request,'tartanzone/manage_group.html',locals())
            m.remove(mobj)
        course = get_object_or_404(Course, id=course_id)
        c = course
        groupobjs = Group.objects.all
        gform = NewGroupForm()
        user = get_object_or_404(TartanUser, user=request.user)
        return render(request,'tartanzone/manage_group.html',locals())
    else:
        return HttpResponse("you have no access to this page")


@csrf_exempt
def delete_group(request):
    if (request.method == "POST"):
        action = request.POST.get("action")
        gname = request.POST.get("groupname")
        try:
            g = get_object_or_404(Group, name = gname)
        except:
            return render(request,'tartanzone/manage_group.html',locals())
        #usern = get_object_or_404(User, username = 'sw')

        if(action == "delete"):
            g.delete()
        if(action == "deletem"):
            m = g.member
            try:
                mname = request.POST.get(gname)
            except:
                return render(request,'tartanzone/manage_group.html',locals())

            try:
                mobj = get_object_or_404(TartanUser, user = get_object_or_404(User, username = mname))
            except:
                return render(request,'tartanzone/manage_group.html',locals())

            m.remove(mobj)
    course = Course.objects.all()
    c = course
    groupobjs = Group.objects.all
    gform = NewGroupForm()
    try:
        user = get_object_or_404(TartanUser, user=request.user)
    except:
        return render(request,'tartanzone/manage_group.html',locals())
    # context['course']=course
    return render(request,'tartanzone/manage_group.html',locals())


@csrf_exempt
def quit_group(request, gname):
    if request.method == "POST":
        action = request.POST.get("action")
        # gname = request.POST.get("groupname")
        try:
            g = get_object_or_404(Group, name = gname)
        except:
            return HttpResponse("do not have group member, please try again ")
        m = g.member
        try:
            mobj = get_object_or_404(TartanUser, user = request.user)
        except:
            return render(request,'tartanzone/manage_group.html',locals())
        m.remove(mobj)

        tartanuser = request.user.tartanuser
        groups = tartanuser.group_set.all()
        # g = Group.objects.filter(user = request.user)
    return redirect(reverse('my_group'))

@csrf_exempt
def join_group(request, course_id):
    context = {}
    course = get_object_or_404(Course, id=course_id)

    data = {}
    review=course.review.all()
    instructor = course.instructor.all()
    if (request.method == "POST"):
        action = request.POST.get("action")
        gname = request.POST.get("groupname")

        g = get_object_or_404(Group, name = gname)
        print(gname)
        #usern = User.objects.get(username = 'sw')
        # if(action == "join"):

        print(action)

        if(action == "quit"):
            m = g.member
            try:
                mobj = get_object_or_404(TartanUser, user = request.user)
            except:
                return render(request,'tartanzone/my_course_review.html',locals())
            m.remove(mobj)

            c = course
            groupobjs = Group.objects.filter(course = c)
            return render(request,'tartanzone/my_course_review.html',locals())
        else:
            print("join")
            u = get_object_or_404(TartanUser, user = request.user) #after implementing user authentication, it should be current user
            uu = get_object_or_404(User, username = u)
            c = course
            # messages.info(request, 'member already exist!')
            groupobjs = Group.objects.filter(course = c)
            gform = NewGroupForm()
            user = get_object_or_404(TartanUser, user=request.user)
            data['error'] = "member already exist!"

            print("error1")
            if(g.member.filter(user = uu)):
                # messages.info(request, 'member already exist!')
                c = course
                groupobjs = Group.objects.filter(course = c)
                gform = NewGroupForm()
                user = get_object_or_404(TartanUser, user=request.user)
                data['error'] = "member already exist!"

                print("error2")
            else:
                g.member.add(u)
                data['error'] = ""
                data['user'] = uu.username

            return JsonResponse(data)

    c = course
    groupobjs = Group.objects.filter(course = c)
    gform = NewGroupForm()

    user = get_object_or_404(TartanUser, user=request.user)

    # context['course']=course
    # return redirect(reverse('course_review',args=[course_id]))
    return render(request,'tartanzone/my_course_review.html',locals())
        # return redirect(reverse("course_review"), c.id)



def home(request):
    context={}
    course=Course.objects.all()
    context['course']=course
    instructor=Instructor.objects.filter(id__lte=6)
    context['instructor']=instructor
    return render(request, 'tartanzone/home.html', context)

@login_required
def all_courses(request):

    context={}
    user=request.user
    try:
        tartanuser = get_object_or_404(TartanUser, user=user)
    except:
        return render(request,'tartanzone/all_courses.html',context)
    course = Course.objects.all()
    context['course']=course
    c = CourseForm()
    context['form']=c
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student
    context['user'] = user
    context['userform']=UserForm()
    return render(request,'tartanzone/all_courses.html',context)


@login_required
def course_review(request,course_id):
    context = {}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student
    course = get_object_or_404(Course, id=course_id)
    context['course']=course
    review=course.review.all().order_by("-agree")
    review = review[:3]
    context['review'] = review
    context['instructor']=course.instructor.all()
    form=ScheduleForm()
    context['form']=form
    context['userform']=UserForm()
    review_num = course.review.all().count()
    five_num = 0
    four_num = 0
    three_num = 0
    two_num = 0
    one_num = 0
    total_score = 0
    for r in course.review.all():
        total_score += r.score
        if r.score == 5:
            five_num += 1
        if r.score == 4:
            four_num += 1
        if r.score == 3:
            three_num += 1
        if r.score == 2:
            two_num += 1
        if r.score == 1:
            one_num += 1
    if review_num == 0:
        context['review_num'] = 0
        context['five_num'] = 0
        context['four_num'] = 0
        context['three_num'] = 0
        context['two_num'] = 0
        context['one_num'] = 0
        context['five_ratio'] = 0
        context['four_ratio'] = 0
        context['three_ratio'] = 0
        context['two_ratio'] = 0
        context['one_ratio'] = 0
        context['average_score'] = 0
        average_star = 0
    else:
        average_score = float('%.2f' % (total_score / review_num))
        context['review_num'] = review_num
        context['five_num'] = five_num
        context['four_num'] = four_num
        context['three_num'] = three_num
        context['two_num'] = two_num
        context['one_num'] = one_num
        context['five_ratio'] = int((five_num / review_num) * 100)
        context['four_ratio'] = int((four_num / review_num) * 100)
        context['three_ratio'] = int((three_num / review_num) * 100)
        context['two_ratio'] = int((two_num / review_num) * 100)
        context['one_ratio'] = int((one_num / review_num) * 100)
        context['average_score'] = average_score
        average_star = int(round(average_score))
    if average_star == 5:
        context['five_average'] = True
    elif average_star == 4:
        context['four_average'] = True
    elif average_star == 3:
        context['three_average'] = True
    elif average_star == 2:
        context['two_average'] = True
    else:
        context['one_average'] = True

    c = course
    groupobjs = Group.objects.filter(course = c)
    context['groupobjs'] = groupobjs
    # if request.method == "POST":
    gform = NewGroupForm()
    context['gform'] = gform
    context['user'] = tartanuser

    return render(request,'tartanzone/course_review.html',context)



@login_required
def add_course(request):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    if tartanuser.role=='administrator':
        admin=0
        student=0
        if tartanuser.role=='administrator':
            admin=1
        if tartanuser.role=='student':
            student=1
        context['admin']=admin
        context['student']=student
        if request.POST:
            c=CourseForm(request.POST, request.FILES)
            if c.is_valid():
                cour = c.save()
                try:
                    print("ssss" + cour.course_img.url)
                except:
                    cour.delete()
                    return HttpResponse("course image field is required!")
                cour.data_event = random.randint(1,5)
                cour.save()
            course = Course.objects.all()
            context['course']=course
            return redirect(reverse("all_courses"))
        c=CourseForm()
        context['form']=c
        return render(request,"tartanzone/add_course.html",context)
    else:
        return HttpResponse("you have no access to this page")

@login_required
def ajax_add_course(request):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    if tartanuser.role=='administrator':
        admin=0
        student=0
        if tartanuser.role=='administrator':
            admin=1
        if tartanuser.role=='student':
            student=1
        context['admin']=admin
        context['student']=student
        data={}
        if request.POST:
            data['error']=""
            c=CourseForm(request.POST, request.FILES)
            if c.is_valid():
                data['error'] = ""
            else:
                print(c.errors)
                data['error'] = c.errors
            return JsonResponse(data,safe=False)
        c=CourseForm()
        context['form']=c
        context['course']=course
        return render(request,"tartanzone/all_course.html",context)
    else:
        return HttpResponse("you have no access to this page")

@login_required
def edit_course(request,course_id):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    if tartanuser.role=='administrator':
        admin=0
        student=0
        if tartanuser.role=='administrator':
            admin=1
        if tartanuser.role=='student':
            student=1
        context['admin']=admin
        context['student']=student
        cc = get_object_or_404(Course, id=course_id)
        course=Course.objects.all()
        context['course']=course

        # c=CourseForm()

        if request.POST:
            cc.code=request.POST['course_code']
            cc.name=request.POST['course_name']
            cc.semester=request.POST['course_semester']
            cc.description=request.POST['course_description']
            cc.save()
        c=CourseForm()
        context['form']=c
        return render(request,'tartanzone/all_courses.html',context)
    else:
        return HttpResponse("you have no access to this page")


@login_required
def edit_instructor(request,instructor_id):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    if tartanuser.role=='administrator':
        admin=0
        student=0
        if tartanuser.role=='administrator':
            admin=1
        if tartanuser.role=='student':
            student=1
        context['admin']=admin
        context['student']=student
        ii = get_object_or_404(Instructor, id=instructor_id)
        instructor=Instructor.objects.all()
        context['instructor']=instructor

        if request.POST:

            ii.name=request.POST['course_name']
            ii.description=request.POST['course_description']
            ii.save()

        return render(request,'tartanzone/all_instructor.html',context)
    else:
        return HttpResponse("you have no access to this page")

@login_required
def delete_instructor(request,instructor_id):
    context={}
    user = request.user
    tartanuser=get_object_or_404(TartanUser,user=user)
    if tartanuser.role=='administrator':
        c=get_object_or_404(Instructor, id=instructor_id)
        c.delete()
        allinstructor = Instructor.objects.all()
        context['instructor']=allinstructor
        return redirect(reverse("all_instructor"))
    else:
        return HttpResponse("you have no access to this page")

@login_required
def update_course(request,course_id):
    context={}
    user = request.user
    tartanuser=get_object_or_404(TartanUser,user=user)
    if tartanuser.role=='administrator':
        course = get_object_or_404(Course, id=course_id)
        if request.POST:
            c=CourseForm(request.POST,instance=course)
            if c.is_valid():
                course=c.save()
                course.save()
            allcourse = Course.objects.all()
            context['course']=allcourse
        return redirect(reverse("all_courses"))
    else:
        return HttpResponse("you have no access to this page")

@login_required
def delete_course(request,course_id):
    context={}
    user = request.user
    tartanuser=get_object_or_404(TartanUser,user=user)
    if tartanuser.role=='administrator':
        c=get_object_or_404(Course, id=course_id)
        c.delete()
        allcourse = Course.objects.all()
        context['course']=allcourse
        return redirect(reverse("all_courses"))
    else:
        return HttpResponse("you have no access to this page")


@login_required
def my_group(request):
    context={}
    course = Course.objects.all()

    tartanuser = request.user.tartanuser
    groups = tartanuser.group_set.all()
    context['group']=groups
    context['userform']=UserForm()
    return render(request, 'tartanzone/my_group.html', context)


@login_required
def group_discussion(request, group_id, post_id):
    ctx = {}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    group = get_object_or_404(Group, id = group_id)

    if tartanuser in group.member.all():
        post = get_object_or_404(DiscussionPost, id = post_id)
        owner = post.student
        if (tartanuser==owner):
            ctx['owner']=1
        else:
            ctx['owner']=0

        if DiscussionPost.objects.filter(id = post_id).count() > 0:
            post = get_object_or_404(DiscussionPost, id = post_id)
            ctx['post'] = post

        ctx['group'] = group
        today = DiscussionPost.objects.filter(group = group, time = datetime.today())
        ctx['today'] = today

        one_day_ago = datetime.today() - timedelta(days=1)
        print(one_day_ago)
        yesterday = DiscussionPost.objects.filter(group = group, time=one_day_ago)
        ctx['yesterday'] = yesterday

        one_week_ago = datetime.today() - timedelta(days=7)
        thisweek = DiscussionPost.objects.filter(group = group, time__range=[one_week_ago, one_day_ago])
        ctx['thisweek'] = thisweek

        moreolder = DiscussionPost.objects.filter(group = group, time__lt=one_week_ago)
        ctx['moreolder'] = moreolder

        if request.method == 'POST':
            if 'submit-answer' in request.POST:
                post = get_object_or_404(DiscussionPost, id = post_id)
                answer = PostAnswer(student=request.user.tartanuser, post=post, content=request.POST['textarea'])
                answer.save()

        return render(request, 'tartanzone/discussion.html', ctx)

    else:
        return HttpResponse("you have no access to this page")

@login_required
def group_discussion1(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    tartanuser = get_object_or_404(TartanUser, user=request.user)

    if tartanuser in group.member.all():

        ctx = {}
        ctx['group'] = group
        today = DiscussionPost.objects.filter(group = group, time = datetime.today())
        ctx['today'] = today

        one_day_ago = datetime.today() - timedelta(days=1)
        print(one_day_ago)
        yesterday = DiscussionPost.objects.filter(group = group, time=one_day_ago)
        ctx['yesterday'] = yesterday

        one_week_ago = datetime.today() - timedelta(days=7)
        thisweek = DiscussionPost.objects.filter(group = group, time__range=[one_week_ago, one_day_ago])
        ctx['thisweek'] = thisweek

        moreolder = DiscussionPost.objects.filter(group = group, time__lt=one_week_ago)
        ctx['moreolder'] = moreolder

        return render(request, 'tartanzone/discussion.html', ctx)

    else:
        return HttpResponse("you have no access to this page")

@login_required
def reply_postanswer(request, group_id, post_id, answer_id):
    group = get_object_or_404(Group, id = group_id)
    post = get_object_or_404(DiscussionPost, id = post_id)
    if request.method == "POST":
        if "reply-submit" in request.POST:
            answer = get_object_or_404(PostAnswer, id = answer_id)
            reply = PostAnswerReply(student=request.user.tartanuser, postanswer=answer, content=request.POST['reply-textarea'])
            reply.save()

    ctx = {}
    if DiscussionPost.objects.filter(id = post_id).count() > 0:
        post = get_object_or_404(DiscussionPost, id = post_id)
        ctx['post'] = post

    ctx['group'] = group
    today = DiscussionPost.objects.filter(group = group, time = datetime.today())
    ctx['today'] = today

    one_day_ago = datetime.today() - timedelta(days=1)
    yesterday = DiscussionPost.objects.filter(group = group, time=one_day_ago)
    ctx['yesterday'] = yesterday

    one_week_ago = datetime.today() - timedelta(days=7)
    thisweek = DiscussionPost.objects.filter(group = group, time__range=[one_week_ago, one_day_ago])
    ctx['thisweek'] = thisweek

    moreolder = DiscussionPost.objects.filter(group = group, time__lt=one_week_ago)
    ctx['moreolder'] = moreolder

    return render(request, 'tartanzone/discussion.html', ctx)

@login_required
def delete_postanswer(request, group_id, post_id, answer_id):
    group = get_object_or_404(Group, id = group_id)
    post = get_object_or_404(DiscussionPost, id = post_id)
    if PostAnswer.objects.filter(id = answer_id).count() > 0:
        answer = get_object_or_404(PostAnswer, id = answer_id)
        if answer.student.id == request.user.tartanuser.id:
            answer.delete()

    ctx = {}
    if DiscussionPost.objects.filter(id = post_id).count() > 0:
        post = get_object_or_404(DiscussionPost, id = post_id)
        ctx['post'] = post

    ctx['group'] = group
    today = DiscussionPost.objects.filter(group = group, time = datetime.today())
    ctx['today'] = today

    one_day_ago = datetime.today() - timedelta(days=1)
    yesterday = DiscussionPost.objects.filter(group = group, time=one_day_ago)
    ctx['yesterday'] = yesterday

    one_week_ago = datetime.today() - timedelta(days=7)
    thisweek = DiscussionPost.objects.filter(group = group, time__range=[one_week_ago, one_day_ago])
    ctx['thisweek'] = thisweek

    moreolder = DiscussionPost.objects.filter(group = group, time__lt=one_week_ago)
    ctx['moreolder'] = moreolder

    return render(request, 'tartanzone/discussion.html', ctx)


@login_required
def new_post(request, group_id):
    group = get_object_or_404(Group, id = group_id)

    if request.method == "GET":
        ctx = {}
        ctx['group'] = group
        today = DiscussionPost.objects.filter(group = group, time = datetime.today())
        ctx['today'] = today

        one_day_ago = datetime.today() - timedelta(days=1)
        yesterday = DiscussionPost.objects.filter(group = group, time=one_day_ago)
        ctx['yesterday'] = yesterday

        one_week_ago = datetime.today() - timedelta(days=7)
        thisweek = DiscussionPost.objects.filter(group = group, time__range=[one_week_ago, one_day_ago])
        ctx['thisweek'] = thisweek

        moreolder = DiscussionPost.objects.filter(group = group, time__lt=one_week_ago)
        ctx['moreolder'] = moreolder

        return render(request, 'tartanzone/new_post.html', ctx)

    if request.method == "POST":

        if 'post-title' in request.POST and 'post-content' in request.POST:
            post = DiscussionPost(student=request.user.tartanuser, group=group, name=request.POST['post-title'], content=request.POST['post-content'])
            post.save()
            post_id = post.id

            ctx = {}
            ctx['group'] = group
            ctx['post'] = post
            today = DiscussionPost.objects.filter(group = group, time = datetime.today())
            ctx['today'] = today

            one_day_ago = datetime.today() - timedelta(days=1)
            yesterday = DiscussionPost.objects.filter(group = group, time = one_day_ago)
            ctx['yesterday'] = yesterday

            one_week_ago = datetime.today() - timedelta(days=7)
            thisweek = DiscussionPost.objects.filter(group = group, time=one_day_ago)
            ctx['thisweek'] = thisweek

            moreolder = DiscussionPost.objects.filter(group = group, time__lt=one_week_ago)
            ctx['moreolder'] = moreolder

            return render(request, 'tartanzone/discussion.html', ctx)


def register(request):

    if request.method == "GET":
        user_form = UserForm()
        return render(request, 'tartanzone/register.html', {'user_form': user_form})

    if request.method == 'POST':
        ctx={}
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # my_group = get_object_or_404(Group, name='student')
            # my_group.user_set.add(user)

            tartanuser = TartanUser(user=user, role='student')
            tartanuser.save()
            auth.login(request, user)
            return redirect(reverse("all_courses"))

        ctx["user_form"] = user_form
        return render(request, 'tartanzone/register.html', ctx)

def login(request):
    context = {}
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None and user.is_active:
            auth.login(request,user)
            course = Course.objects.all()
            context['course']=course
            return redirect(reverse('all_courses'))

        else:
            context['message'] = 'Wrong password. Please try again'
            return render(request,'tartanzone/home.html',context)

    return render(request,'tartanzone/home.html',context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


@login_required
def add_to_my_course(request,course_id):
    context = {}
    user = request.user
    print(user)
    course = get_object_or_404(Course, id=course_id)
    tartanuser = get_object_or_404(TartanUser, user=user)
    tartanuser.course.add(course)
    context['course']=tartanuser.course.all()
    return redirect(reverse("my_course"))

@login_required
def leave_review(request,course_id):
    context = {}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    course=get_object_or_404(Course, id=course_id)
    if request.POST:
        content = request.POST.get('message')
        if len(content) > 900:
            context['error'] = "The reivew is too long!"
            context['course']=course
            return redirect(reverse('course_review',args=[course_id]))
        score = int(request.POST['review-score'])
        review = Review(student=tartanuser,course=course,content=content, score=score)
        if score == 5:
            review.five_star = True
            review.four_star = False
            review.three_star = False
            review.two_star = False
            review.one_star = False
        if score == 4:
            review.five_star = False
            review.four_star = True
            review.three_star = False
            review.two_star = False
            review.one_star = False
        if score == 3:
            review.five_star = False
            review.four_star = False
            review.three_star = True
            review.two_star = False
            review.one_star = False
        if score == 2:
            review.five_star = False
            review.four_star = False
            review.three_star = False
            review.two_star = True
            review.one_star = False
        if score == 1:
            review.five_star = False
            review.four_star = False
            review.three_star = False
            review.two_star = False
            review.one_star = True
        review.save()
        context['course']=course
        return redirect(reverse('course_review',args=[course_id]))

@login_required
def my_course(request):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    context['course']=tartanuser.course.all()
    context['userform']=UserForm()
    return render(request,'tartanzone/my_course.html',context)

@login_required
def my_course_review(request,course_id):
    context = {}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student
    course = get_object_or_404(Course, id=course_id)
    context['course']=course
    review=course.review.all().order_by("-agree")
    review = review[:3]
    context['review'] = review
    context['instructor']=course.instructor.all()
    form=ScheduleForm()
    context['form']=form

    review_num = course.review.all().count()
    five_num = 0
    four_num = 0
    three_num = 0
    two_num = 0
    one_num = 0
    total_score = 0
    for r in course.review.all():
        total_score += r.score
        if r.score == 5:
            five_num += 1
        if r.score == 4:
            four_num += 1
        if r.score == 3:
            three_num += 1
        if r.score == 2:
            two_num += 1
        if r.score == 1:
            one_num += 1
    if review_num == 0:
        context['review_num'] = 0
        context['five_num'] = 0
        context['four_num'] = 0
        context['three_num'] = 0
        context['two_num'] = 0
        context['one_num'] = 0
        context['five_ratio'] = 0
        context['four_ratio'] = 0
        context['three_ratio'] = 0
        context['two_ratio'] = 0
        context['one_ratio'] = 0
        context['average_score'] = 0
        average_star = 5
    else:
        average_score = float('%.2f' % (total_score / review_num))
        context['review_num'] = review_num
        context['five_num'] = five_num
        context['four_num'] = four_num
        context['three_num'] = three_num
        context['two_num'] = two_num
        context['one_num'] = one_num
        context['five_ratio'] = int((five_num / review_num) * 100)
        context['four_ratio'] = int((four_num / review_num) * 100)
        context['three_ratio'] = int((three_num / review_num) * 100)
        context['two_ratio'] = int((two_num / review_num) * 100)
        context['one_ratio'] = int((one_num / review_num) * 100)
        context['average_score'] = average_score
        average_star = int(round(average_score))
    if average_star == 5:
        context['five_average'] = True
    elif average_star == 4:
        context['four_average'] = True
    elif average_star == 3:
        context['three_average'] = True
    elif average_star == 2:
        context['two_average'] = True
    else:
        context['one_average'] = True

    c = course
    groupobjs = Group.objects.filter(course = c)
    context['groupobjs'] = groupobjs
    # if request.method == "POST":
    gform = NewGroupForm()
    context['gform'] = gform
    context['user'] = tartanuser

    return render(request,'tartanzone/my_course_review.html',context)


@login_required
def drop_course(request,course_id):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    course=get_object_or_404(Course, id=course_id)
    tartanuser.course.remove(course)
    context[course]=tartanuser.course.all()
    return redirect(reverse('my_course'))

@login_required
def instructor_profile(request,instructor_id):
    context={}
    instructor=get_object_or_404(Instructor, id=instructor_id)
    context['instructor']=instructor
    courses=instructor.course_set.all()
    context['courses']=courses
    return render(request,'tartanzone/instructor_profile.html',context)

@login_required
def all_instructor(request):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student
    instructor=Instructor.objects.all()
    context['instructor']=instructor
    form=InstructorForm()
    context['form']=form
    context['userform']=UserForm()
    return render(request,'tartanzone/all_instructor.html',context)

@login_required
def add_instructor(request):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser,user=user)
    if tartanuser.role=='administrator':
        if request.POST:
            c=InstructorForm(request.POST,request.FILES)
            if c.is_valid():
                ins = c.save()
                try:
                    print(ins.instructor_img.url)
                except:
                    ins.delete()
                    return HttpResponse("instructor image is required!")
                instructor = Instructor.objects.all()
                context['instructor']=instructor
                return redirect(reverse("all_instructor"))
            else:
                instructor = Instructor.objects.all()
                context['instructor'] = instructor
                # print('-------------')
                # if 'name' in c.errors.keys():
                    # print(c.errors['name'].as_text())
                    # messages.warning(request, 'Add instructor failed: ' + c.errors['name'].as_text()[1:])
                # c = InstructorForm()
                # context['form'] = c
                # return render(request, "tartanzone/all_instructor.html", context)
                return redirect(reverse("all_instructor"))

        c=InstructorForm()
        context['form']=c
        return render(request,"tartanzone/all_instructor.html",context)
    else:
        return HttpResponse("you have no access to this page")

@login_required
def ajax_add_instructor(request):
    print("entering ajax add")
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    if tartanuser.role=='administrator':
        admin=0
        student=0
        if tartanuser.role=='administrator':
            admin=1
        if tartanuser.role=='student':
            student=1
        context['admin']=admin
        context['student']=student
        data = {}
        if request.POST:
            i=InstructorForm(request.POST, request.FILES)
            if i.is_valid():
                data['error'] = ""
            else:
                # data={}
                data['error'] = i.errors

            return JsonResponse(data,safe=False)
        i=InstructorForm()
        instructor=Instructor.objects.all()
        context['form']=i
        context['instructor']=instructor
        return render(request,"tartanzone/all_instructor.html",context)
    else:
        return HttpResponse("you have no access to this page")


@login_required
def delete_review(request,review_id,course_id):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    if tartanuser.role=='administrator':
        admin=0
        student=0
        if tartanuser.role=='administrator':
            admin=1
        if tartanuser.role=='student':
            student=1
        context['admin']=admin
        context['student']=student
        review=get_object_or_404(Review, id=review_id)
        review.delete()
        course=get_object_or_404(Course, id=course_id)
        context['course']=course
        instructor=course.instructor.all()
        context['instructor']=instructor
        return redirect(reverse('course_review',args=[course_id]))
    else:
        return HttpResponse("you have no access to this page")

@login_required
def search_course(request):
    context = {}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student
    # context['course'] = Course.objects.all()

    if request.method == "POST":
        if "search-by" in request.POST and "search-input" in request.POST:
            if request.POST['search-by'] == "name":
                name = request.POST['search-input']
                course_byname = Course.objects.filter(name__startswith=name)
                if course_byname.count() > 0:
                    context['course'] = course_byname
                    context['search'] = 'Search courses by name: ' + '"' + name + '"'
                else:
                    context['no_found_name'] = True

                return render(request,'tartanzone/all_courses.html',context)

            if request.POST['search-by'] == "code":
                code = request.POST['search-input']
                course_bycode = Course.objects.filter(code__startswith=code)
                if course_bycode.count() > 0:
                    context['course'] = course_bycode
                    context['search'] = 'Search courses by code: ' + '"' + code + '"'
                else:
                    context['no_found_code'] = True

                return render(request,'tartanzone/all_courses.html',context)

            if request.POST['search-by'] == "day":
                days = request.POST['search-input']
                courseday = []
                weekdayDic = {}

                weekdayDic['Monday'] = 'Mon'
                weekdayDic['Tuesday'] = 'Tue'
                weekdayDic['Wednesday'] = 'Weds'
                weekdayDic['Thursday'] = 'Thu'
                weekdayDic['Friday'] = 'Fri'
                weekdayDic['Saturday'] = 'Sat'
                weekdayDic['Sunday'] = 'Sun'

                if 'M' in days or 'm' in days:
                    courseday.append("Monday")

                if 'T' in days or 't' in days:
                    courseday.append("Tuesday")

                if 'W' in days or 'w' in days:
                    courseday.append("Wednesday")

                if 'R' in days or 'r' in days:
                    courseday.append("Thursday")

                if 'F' in days or 'f' in days:
                    courseday.append("Friday")

                if len(courseday) == 5:
                    filter_result = Course.objects.all()

                    if filter_result.count() > 0:
                        context['course'] = filter_result
                        context['search'] = 'Filter result for courses in: ' + str(', '.join(courseday))
                    else:
                        context['no_found_day'] = True

                    return render(request, 'tartanzone/all_courses.html', context)

                if len(courseday) == 0:
                    context['no_found_day'] = True
                    return render(request, 'tartanzone/all_courses.html', context)

                init = 0
                for x in courseday:
                    if init:
                        temp_filter_result = Course.objects.filter(schedule__weekday=str(weekdayDic[x]))
                        filter_result = filter_result | temp_filter_result
                    else:
                        init = 1
                        filter_result = Course.objects.filter(schedule__weekday=str(weekdayDic[x]))


                if filter_result.count() > 0:
                    context['course'] = filter_result
                    context['search'] = 'Filter result for courses in: ' + str(', '.join(courseday))
                else:
                    context['no_found_day'] = True

                return render(request, 'tartanzone/all_courses.html', context)

            if request.POST['search-by'] == "quota":
                quota = request.POST['search-input']
                quota = str(quota)

                if quota == '~':
                    filter_result = Course.objects.all()
                    if filter_result.count() > 0:
                        context['course'] = filter_result
                        context['search'] = 'Filter result for courses quota between: ' + str(quota)
                    else:
                        context['no_found_quota'] = True
                    return render(request, 'tartanzone/all_courses.html', context)

                quota = quota.strip().split('~')

                if len(quota) == 1:
                    if not quota[0]:
                        quota_min = -1
                    else:
                        quota_min = int(quota[0])

                    quota_max = -1

                else:
                    if quota[0]:
                        quota_min = int(quota[0])
                    else:
                        quota_min = -1

                    if quota[1]:
                        quota_max = int(quota[1])
                    else:
                        quota_max = -1

                if quota_max == -1 and quota_min > 0:
                    filter_result = Course.objects.filter(quota__gte=quota_min)
                if quota_max > 0 and quota_min == -1:
                    filter_result = Course.objects.filter(quota__lte=quota_max)
                if quota_max > 0 and quota_min > 0:
                    filter_result = Course.objects.filter(quota__gte=quota_min, quota__lte=quota_max)

                if filter_result.count() > 0:
                    context['course'] = filter_result
                    context['search'] = 'Filter result for courses quota between: ' + str(' ~ '.join(quota))
                else:
                    context['no_found_quota'] = True

                return render(request, 'tartanzone/all_courses.html', context)


            if request.POST['search-by'] == "semester":
                semester = request.POST['search-input']
                if semester:
                    course_bysemester = Course.objects.filter(semester=semester)

                    if course_bysemester.count() > 0:
                        context['course'] = course_bysemester
                        context['search'] = 'Search courses by semester: ' + '"' + str(semester) + '"'
                    else:
                        context['no_found_semester'] = True

                    return render(request, 'tartanzone/all_courses.html', context)

                else:
                    course_bysemester = Course.objects.all()
                    if course_bysemester.count() > 0:
                        context['course'] = course_bysemester
                        context['search'] = 'Search courses by semester: ' + '"' + str(semester) + '"'
                    else:
                        context['no_found_semester'] = True

        return render(request,'tartanzone/all_courses.html',context)

@login_required
def search_instructor(request):
    context = {}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student

    if request.method == "POST":
        if "search-name" in request.POST:
            name = request.POST['search-name-input']
            instructor_byname = Instructor.objects.filter(name__startswith=name)
            if instructor_byname.count() > 0:
                context['instructor'] = instructor_byname
                context['search'] = 'Search instructor by name starting with: ' + '"' + name + '"'
            else:
                context['no_found_name'] = True

            return render(request,'tartanzone/all_instructor.html',context)

        if "search-school" in request.POST:
            school = request.POST['search-school-input']
            instructor_byschool = Instructor.objects.filter(school=school)
            schoolDic = {}
            schoolDic['SCS'] = 'School of Computer Science'
            schoolDic['ENG'] = 'College of Engineering'
            schoolDic['ART'] = 'College of Fine Arts'
            schoolDic['HSS'] = 'Dietrich College of Humanities & Social Sciences'
            schoolDic['HEI'] = 'Heinz College of Information Systems and Public Policy'
            schoolDic['SCI'] = 'Mellon College of Science'
            schoolDic['TEP'] = 'Tepper School of Business'

            if instructor_byschool.count() > 0:
                context['instructor'] = instructor_byschool
                context['search'] = 'Search instructor by school: ' + '"' + schoolDic[school] + '"'
            else:
                context['no_found_code'] = True

            return render(request,'tartanzone/all_instructor.html',context)

@login_required
def ajax_agree(request):
    if request.method == "POST":
        data = {}
        review_id = request.POST["review_id"]
        review = get_object_or_404(Review, id=review_id)
        pre_agree = ReviewAgree.objects.filter(review=review, student=request.user.tartanuser)
        if pre_agree.count() == 0:
            data['success'] = "yes"
            review.agree += 1;
            review.save()

            agree = ReviewAgree(review=review, student=request.user.tartanuser)
            agree.save()
            data["agree_num"] = review.agree

        elif pre_agree.count() > 0:
            data['success'] = 'no'
            data["agree_num"] = review.agree

        return JsonResponse(data)

@login_required
def ajax_disagree(request):
    if request.method == "POST":
        data = {}
        review_id = request.POST["review_id"]
        review = get_object_or_404(Review, id=review_id)
        pre_agree = ReviewAgree.objects.filter(review=review, student=request.user.tartanuser)
        if pre_agree.count() == 0:
            data['success'] = "no"
            data["agree_num"] = review.agree

        elif pre_agree.count() > 0:

            if review.agree > 0:
                data['success'] = "yes"
                review.agree -= 1;
                review.save()
            else:
                data['success'] = "mistake"

            agree = get_object_or_404(ReviewAgree, review=review, student=request.user.tartanuser)
            agree.delete()
            data["agree_num"] = review.agree

        return JsonResponse(data)

@login_required
def scheduel(request):
    context = {}
    conflict = []
    tartanuser = request.user.tartanuser
    course = tartanuser.course.all()
    Monday = []
    Tuesday=[]
    Wednesday=[]
    Thursday=[]
    Friday=[]
    for c in course:
        for s in c.schedule.all():
            if s.weekday == "Mon":
                t=Temp(course=c.name,weekday="Mon",starttime=s.starttime,endtime=s.endtime, data_event = c.data_event)
                t.save()
                Monday.append(t)
            if s.weekday == "Tue":
                t=Temp(course=c.name,weekday="Tue",starttime=s.starttime,endtime=s.endtime, data_event = c.data_event)
                t.save()
                Tuesday.append(t)
            if s.weekday == "Weds":
                t=Temp(course=c.name,weekday="Weds",starttime=s.starttime,endtime=s.endtime, data_event = c.data_event)
                t.save()
                Wednesday.append(t)
            if s.weekday == "Thu":
                t=Temp(course=c.name,weekday="Thu",starttime=s.starttime,endtime=s.endtime, data_event = c.data_event)
                t.save()
                Thursday.append(t)
            if s.weekday == "Fri":
                t=Temp(course=c.name,weekday="Fri",starttime=s.starttime,endtime=s.endtime, data_event = c.data_event)
                t.save()
                Friday.append(t)
    n = len(Monday)
    for i in range(n - 1):
        s = int(Monday[i].starttime[0:2]) * 60 + int(Monday[i].starttime[3:5])
        e = int(Monday[i].endtime[0:2]) * 60 + int(Monday[i].endtime[3:5])
        for j in range(i + 1, n):
            ss = int(Monday[j].starttime[0:2]) * 60 + int(Monday[j].starttime[3:5])
            ee = int(Monday[j].endtime[0:2]) * 60 + int(Monday[j].endtime[3:5])
            if (ss >= s and ss < e) or (s >= ss and s < ee):
                conflict.append(Monday[i].course + " V.S. " + Monday[j].course + " on Monday")
    n = len(Tuesday)
    for i in range(n - 1):
        s = int(Tuesday[i].starttime[0:2]) * 60 + int(Tuesday[i].starttime[3:5])
        e = int(Tuesday[i].endtime[0:2]) * 60 + int(Tuesday[i].endtime[3:5])
        for j in range(i + 1, n):
            ss = int(Tuesday[j].starttime[0:2]) * 60 + int(Tuesday[j].starttime[3:5])
            ee = int(Tuesday[j].endtime[0:2]) * 60 + int(Tuesday[j].endtime[3:5])
            if (ss >= s and ss < e) or (s >= ss and s < ee):
                conflict.append(Tuesday[i].course + " V.S. " + Tuesday[j].course + " on Tuesday")

    n = len(Wednesday)
    for i in range(n - 1):
        s = int(Wednesday[i].starttime[0:2]) * 60 + int(Wednesday[i].starttime[3:5])
        e = int(Wednesday[i].endtime[0:2]) * 60 + int(Wednesday[i].endtime[3:5])
        for j in range(i + 1, n):
            ss = int(Wednesday[j].starttime[0:2]) * 60 + int(Wednesday[j].starttime[3:5])
            ee = int(Wednesday[j].endtime[0:2]) * 60 + int(Wednesday[j].endtime[3:5])
            if (ss >= s and ss < e) or (s >= ss and s < ee):
                conflict.append(Wednesday[i].course + " V.S. " + Wednesday[j].course + " on Wednesday")

    n = len(Thursday)
    for i in range(n - 1):
        s = int(Thursday[i].starttime[0:2]) * 60 + int(Thursday[i].starttime[3:5])
        e = int(Thursday[i].endtime[0:2]) * 60 + int(Thursday[i].endtime[3:5])
        for j in range(i + 1, n):
            ss = int(Thursday[j].starttime[0:2]) * 60 + int(Thursday[j].starttime[3:5])
            ee = int(Thursday[j].endtime[0:2]) * 60 + int(Thursday[j].endtime[3:5])
            if (ss >= s and ss < e) or (s >= ss and s < ee):
                conflict.append(Thursday[i].course + " V.S. " + Thursday[j].course + " on Thursday")

    n = len(Friday)
    for i in range(n - 1):
        s = int(Friday[i].starttime[0:2]) * 60 + int(Friday[i].starttime[3:5])
        e = int(Friday[i].endtime[0:2]) * 60 + int(Friday[i].endtime[3:5])
        for j in range(i + 1, n):
            ss = int(Friday[j].starttime[0:2]) * 60 + int(Friday[j].starttime[3:5])
            ee = int(Friday[j].endtime[0:2]) * 60 + int(Friday[j].endtime[3:5])
            if (ss >= s and ss < e) or (s >= ss and s < ee):
                conflict.append(Friday[i].course + " V.S. " + Friday[j].course + " on Friday")

    context['Monday'] = Monday
    context['Tuesday'] = Tuesday
    context['Wednesday'] = Wednesday
    context['Thursday'] = Thursday
    context['Friday'] = Friday
    if len(conflict) > 0:
        context['conflict'] = conflict
    return render(request, 'tartanzone/scheduel.html', context)

@login_required
def edit_post(request,post_id,group_id):
    context = {}
    post = get_object_or_404(DiscussionPost, id=post_id)
    group = get_object_or_404(Group, id=group_id)
    context['group']=group
    context['post'] = post

    if request.POST:
        post.name = request.POST['post-title']
        post.content = request.POST['post-content']
        post.save()

    return render(request,'tartanzone/discussion.html',context)

@login_required
def all_reviews(request, course_id):
    context = {}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student
    course = get_object_or_404(Course, id=course_id)
    context['course']=course
    review=course.review.all().order_by("-agree")
    context['review'] = review
    if request.POST:
        if "agree" in request.POST:
            return render(request,'tartanzone/all_reviews.html',context)
        if "time" in request.POST:
            review = course.review.all().order_by("-id")
            context['review'] = review
    return render(request,'tartanzone/all_reviews.html',context)

@login_required
def add_schedule(request,course_id):
    context={}
    course=get_object_or_404(Course, id=course_id)
    schedule = Schedule()
    user=request.user
    tartanuser=get_object_or_404(TartanUser,user=user)
    if tartanuser.role=='administrator':
        if request.POST:
            c=ScheduleForm(request.POST,instance=schedule)
            if c.is_valid():
                schedule=c.save()
                schedule.save()
                course.schedule.add(schedule)
            context['course']=course
            return redirect(reverse('course_review',args=[course_id]))
    else:
        return HttpResponse("you have no access to this page")

@login_required
def ajax_add_schedule(request):
    context={}
    user=request.user
    tartanuser=get_object_or_404(TartanUser, user=user)
    admin=0
    student=0
    if tartanuser.role=='administrator':
        admin=1
    if tartanuser.role=='student':
        student=1
    context['admin']=admin
    context['student']=student
    data = {}
    if request.POST:
        # i=InstructorForm(request.POST, request.FILES)
        s=ScheduleForm(request.POST, request.FILES)
        if s.is_valid():
            # ins = i.save()
            # ins.save()
            # ins = Instructor.objects.all()
            # context['instructor']=ins
            # return redirect(reverse("all_instructor"))
            data['error'] = ""
        else:
            # data={}
            data['error'] = s.errors

        return JsonResponse(data,safe=False)
    s=ScheduleForm()
    scheduel=Schedule.objects.all()
    context['form']=s
    context['schedule']=scheduel
    return render(request,"tartanzone/course_review.html",context)

@login_required
def add_admin(request):
    context={}
    tartanuser=get_object_or_404(TartanUser,user=request.user)
    if tartanuser.role=='administrator':
        form=UserForm()
        context['userform']=form
        if request.POST:
            userform=UserForm(request.POST)
            if userform.is_valid():
                user = userform.save()
                user.set_password(user.password)
                user.save()
                # my_group = get_object_or_404(Group, name='student')
                # my_group.user_set.add(user)

                tartanuser = TartanUser(user=user, role='administrator')
                tartanuser.save()
                auth.login(request, user)
                return redirect(reverse("all_courses"))
    else:
        return HttpResponse("you have no access to this page")
