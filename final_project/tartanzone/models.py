from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Instructor(models.Model):
    def validate_even(value):
        if len(value) > 5:
            raise ValidationError(
                _('%(value)s is not an even number'),
                params={'value': value},
            )

    def validate_name_exist(value):
        if (Instructor.objects.filter(name__exact=value).count() > 0):
            raise ValidationError(
                _('%(value)s already exists'),
                params={'value': value},
            )

    SCHOOL = (
        ('SCS', 'School of Computer Science'),
        ('ENG', 'College of Engineering'),
        ('ART', 'College of Fine Arts'),
        ('HSS', 'Dietrich College of Humanities & Social Sciences'),
        ('HEI', 'Heinz College of Information Systems and Public Policy'),
        ('SCI', 'Mellon College of Science'),
        ('TEP', 'Tepper School of Business'),
    )

    name = models.CharField(max_length = 50, validators=[validate_name_exist])
    # photo_url = models.CharField(max_length=500)
    description = models.TextField(max_length=500)
    school = models.CharField(max_length=100, choices=SCHOOL, default='SCS')

    instructor_img = models.ImageField(upload_to='documents/', null=True, blank=True)


    def __str__(self):
        return self.name

def validate_starttime(starttime):
    valid_hour = ['09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
    if len(starttime) != 5 or starttime[2] != ':' or starttime[0:2] not in valid_hour:
        raise ValidationError(
            _('%(value)s is not an acceptable time'),
            params={'value': starttime},
        )

    if int(starttime[3:5]) > 59 or int(starttime[3:5]) < 0:
        raise ValidationError(
            _('%(value)s is not an acceptable time'),
            params={'value': starttime},
        )


def validate_endtime(endtime):
    valid_hour = ['09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
    if len(endtime) != 5 or endtime[2] != ':' or endtime[0:2] not in valid_hour:
        raise ValidationError(
            _('%(value)s is not an acceptable time'),
            params={'value': endtime},
        )

    if int(endtime[3:5]) > 59 or int(endtime[3:5]) < 0:
        raise ValidationError(
            _('%(value)s is not an acceptable time'),
            params={'value': endtime},
        )


class Schedule(models.Model):
    WEEKDAY = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Weds', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
    )
    weekday = models.CharField(max_length=5, choices=WEEKDAY, default='Mon')
    starttime = models.CharField(max_length = 5, default='10:00', validators=[validate_starttime])
    endtime = models.CharField(max_length = 5, default='11:20')

def code_validator(code):
    if code < 10000 or code > 99999:
        raise ValidationError("invalid code: code must between 10000 - 99999.")
    if (Course.objects.filter(code__exact=code).count() > 0):
        raise ValidationError(
            _('%(value)s already exists'),
            params={'value': code},
        )

def name_validator(name):
    if (Course.objects.filter(name__exact=name).count() > 0):
        raise ValidationError(
            _('%(value)s already exists'),
            params={'value': name},
        )


class Course(models.Model):
    code = models.IntegerField(default=10000, validators=[code_validator])
    name = models.CharField(max_length = 50, validators=[name_validator])
    schedule = models.ManyToManyField(Schedule)
    SEM = (
        ('F', 'fall'),
        ('S', 'spring'),
        ('FS', 'fall/spring'),
    )
    semester = models.CharField(max_length = 5, choices=SEM, default='FS')
    instructor = models.ManyToManyField(Instructor)
    quota = models.IntegerField()
    description=models.TextField(max_length=1000)

    course_img = models.ImageField(upload_to='documents/', null=True, blank=True)

    data_event = models.IntegerField(default = 1)

    def __str__(self):
        return self.name


class TartanUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, blank=True)
    role = models.CharField(max_length = 15, choices=[('student','student'),('administrator','adminitrator')],default='student')

    def __str__(self):
        return self.user.username


def groupmember_validator(name):
    if (TartanUser.objects.filter(user__exact=name).count() < 1):
        raise ValidationError(
            _('%(value)s does not exist'),
            params={'value': name},
        )

def groupcourse_validator(name):
    if (Course.objects.filter(name__exact==name).count() < 1):
        raise ValidationError(
            _('%(value)s does not exist'),
            params={'value': name},
        )

class Group(models.Model):
    member = models.ManyToManyField(TartanUser)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='group')
    group_owner = models.ForeignKey(TartanUser,on_delete=models.CASCADE,related_name='group_o')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class DiscussionPost(models.Model):
    student = models.ForeignKey(TartanUser, on_delete=models.CASCADE,related_name='discussionpost')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name='discussionpost')
    time = models.DateField(default=datetime.now)
    name = models.CharField(max_length = 300, default="anonymous")
    content = models.CharField(max_length = 1000)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.content

class Review(models.Model):
    student = models.ForeignKey(TartanUser,on_delete=models.CASCADE,related_name='review')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='review')
    content = models.CharField(max_length = 1000,null=True,blank=True)
    agree = models.IntegerField(default = 0)
    score = models.IntegerField(default = 5)
    five_star = models.BooleanField(default=True)
    four_star = models.BooleanField(default=False)
    three_star = models.BooleanField(default=False)
    two_star = models.BooleanField(default=False)
    one_star = models.BooleanField(default=False)
    time = models.DateField(default=datetime.now)

    def __str__(self):
        return self.content

class PostAnswer(models.Model):
    student = models.ForeignKey(TartanUser, on_delete=models.CASCADE,related_name='postanswer')
    post = models.ForeignKey(DiscussionPost, on_delete=models.CASCADE,related_name='postanswer')
    time = models.DateField(default=datetime.now)
    content = models.CharField(max_length = 1000)

    def __str__(self):
        return self.content

class PostAnswerReply(models.Model):
    student = models.ForeignKey(TartanUser, on_delete=models.CASCADE, related_name='postanswerreply')
    postanswer = models.ForeignKey(PostAnswer, on_delete=models.CASCADE,related_name='postanswerreply')
    time = models.DateField(default=datetime.now)
    content = models.CharField(max_length = 500)

class ReviewAgree(models.Model):
    student = models.ForeignKey(TartanUser, on_delete=models.CASCADE, related_name='reviewagree')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviewagree')


class Temp(models.Model):
    course = models.CharField(max_length=50)
    data_event = models.IntegerField(default=1)
    weekday = models.CharField(max_length=10)
    starttime = models.CharField(max_length=10)
    endtime = models.CharField(max_length=10)
