from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Question, Comment, Session, Record



class ProfileForm(forms.Form):
    '''
    class that creates profile update form
    ''' 
    first_name = forms.CharField(label='First Name',max_length = 30)
    last_name = forms.CharField(label='Last Name',max_length = 30)
    email = forms.EmailField(label='email',max_length = 30)
    phone_number = forms.IntegerField(label = 'Phone Number') 
    addiction = forms.CharField(label='Addiction',max_length = 30)

class QuestionForm(forms.ModelForm):
    '''
    classs that creates profile update form
    '''
    class Meta:
        model = Question
        fields = ['topic','narrative']

class CommentForm(forms.ModelForm):
    '''
    class that creates the comment form
    '''
    class Meta:
        model = Comment
        fields = ['opinion']

class RecordForm(forms.ModelForm):
    '''
    class that creates the patient record form
    '''
    class Meta:
        model = Record
        fields =['problem']
