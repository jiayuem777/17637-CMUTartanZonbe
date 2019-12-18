from django import forms
from .models import Course,Instructor, Group, Schedule
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CourseForm(forms.ModelForm):
    code=forms.IntegerField(min_value=10000, max_value=99999)

    class Meta:
        model = Course
        fields = (
            "code",
            "name",
            "course_img",
            "semester",
            "instructor",
            "description",
            "quota",
        )
    # def clean(self):
        # data from the form is fetched using super function
        # cleaned_data = super().clean()

        # extract the data fields from the data
        # code = cleaned_data.get('code')
        # name = cleaned_data.get('name')
        # quota = cleaned_data.get('quota')
        # description = cleaned_data.get('description')
        # instructor = cleaned_data.get('instructor')

        # conditions to be met for the data
        # if (Course.objects.filter(name__exact=name).count() > 0):
        #     self.add_error('name', 'Course name already exists')
        #
        # if (Course.objects.filter(code=code).count() > 0):
        #     self.add_error('code', 'Course code already exists')
        #
        # if (quota > 0):
        #     self.add_error('code', 'Course code already exists')

        # return any errors if found
        # return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password', 'first_name', 'last_name')


class InstructorForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Instructor Name"}))

    class Meta():
        model = Instructor
        fields = (
            "name",
            # "photo_url",
            "description",
            "instructor_img",
            "school",
        )

    def clean(self):
        # data from the form is fetched using super function
        cleaned_data = super().clean()

        # extract the data fields from the data
        ins_name = cleaned_data.get('name')
        ins_des = cleaned_data.get('description')

        # conditions to be met for the data
        if (Instructor.objects.filter(name__exact=ins_name).count() > 0):
            raise ValidationError('Instructor name already exists')

            # return any errors if found
        return cleaned_data



class NewGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',  'member', 'course')

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        super(NewGroupForm, self).__init__(*args, **kwargs)
        self.fields['member'].required = False
        # self.fields['group_owner'].initial = self.request.user
        # self.fields['groupowner'].initial = request.user


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if( Group.objects.filter(name__exact = name ).count() >0):
            msg = "group already exist, please change name"
            self.add_error('name', msg)
        # price = cleaned_data.get('price')
        # if(dish.objects.filter(_name = cleaned_data['name']).count() > 0):
        #     raise forms.ValidationError("Name is repeat")
        # if(is_number(price)== False):
        #     msg = "Price shoud be int"
        #     self.add_error('price', msg)
            # raise forms.ValidationError("Price shoud be int")

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = (
            "weekday",
            "starttime",
            "endtime"
        )
    def clean_endtime(self):
        # data from the form is fetched using super function
        cleaned_data = super().clean()

        # extract the data fields from the data
        weekday = cleaned_data.get('weekday')
        starttime = cleaned_data.get('starttime')
        endtime = cleaned_data.get('endtime')

        valid_hour = ['09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
        # if len(starttime) != 5 or starttime[2] !=':' or starttime[0:2] not in valid_hour:
        #     raise ValidationError('Input start time invalid')
        # if int(starttime[3:5]) > 59 or int(starttime[3:5]) < 0:
        #     raise ValidationError('Input start time invalid')
        #
        if len(endtime) != 5 or endtime[2] !=':' or endtime[0:2] not in valid_hour:
            raise ValidationError(
                _('%(value)s is not an acceptable time'),
                params={'value': endtime},
            )
        
        if int(endtime[3:5]) > 59 or int(endtime[3:5]) < 0:
            raise ValidationError(
                _('%(value)s is not an acceptable time'),
                params={'value': endtime},
            )

        # conditions to be met for the data
        if int(starttime[0:2]) > int(endtime[0:2]):
            raise ValidationError(
                _('%(value)s (starttime) should not be later than the %(end)s (endtime)'),
                params={'value': starttime, 'end': endtime},
            )

        elif int(starttime[0:2]) == int(endtime[0:2]) and int(starttime[3:5]) >= int(endtime[3:5]):
            raise ValidationError(
                _('%(value)s (starttime) should not be later than the %(end)s (endtime)'),
                params={'value': starttime, 'end': endtime},
            )
            # raise ValidationError('endtime should be later than starttime')

        # return any errors if found
        return endtime

