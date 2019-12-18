from django.contrib import admin

# Register your models here.
from .models import Course,TartanUser,Group,DiscussionPost,Review,Instructor, PostAnswer, PostAnswerReply, ReviewAgree, Schedule

# Register your models here.
admin.site.register(Course)
admin.site.register(TartanUser)
admin.site.register(Group)
admin.site.register(DiscussionPost)
admin.site.register(Review)
admin.site.register(Instructor)
admin.site.register(PostAnswer)
admin.site.register(PostAnswerReply)
admin.site.register(ReviewAgree)
admin.site.register(Schedule)
