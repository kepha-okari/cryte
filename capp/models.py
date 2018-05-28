from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime as dt

# Create your models here.
class Profile(models.Model):
    user_type = models.CharField(max_length=10,default='patient')
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 10,blank =True)
    addiction = models.CharField(max_length = 200,blank =True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    def save_profile(self):
        '''
        Method that saves a given profile to the database
        '''
        self.save()
        

    @classmethod
    def get_profile(cls,user_id):
        '''
        Method that searches for a particular user
        '''
        profile = cls.objects.get(user=user_id)
        return profile


class Record(models.Model):
    date_checked = models.DateTimeField(auto_now_add=True, null=True)
    problem = models.CharField(max_length = 200)
    Recurrent = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @classmethod
    # def get_records(cls,):
    #     count = cls.objects.filter(id=user_id)
    #     return len(count)

    @classmethod
    def get_records(cls,):
        records = cls.objects.all()
        return records

class Appointment(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class Question(models.Model):
    topic = models.CharField(max_length=150, null=True, blank=True)
    narrative = models.CharField(max_length=300, null=True, blank=True)
    date_asked = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_questions(cls):
        questions = cls.objects.all()
        return questions

    @classmethod
    def get_specific_question(cls,question_id):
        question = cls.objects.get(pk=question_id)
        return question



class Comment(models.Model):
    opinion = models.CharField(max_length=200,null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(Question,null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_comments(cls,question_id):
        comments = cls.objects.filter(question=question_id)
        return comments

class Doctor(models.Model):
    name = models.CharField(max_length=30)
    speciality = models.CharField(max_length=30,default='Psychology')


class Session(models.Model):
    Availability = models.BooleanField(default=True)
    sloted_date = models.DateTimeField(blank=True, null=True)
    duration = models.CharField( max_length=30, blank=True,null=True)
    doctor = models.ForeignKey(Doctor,null =True,blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User,null =True,blank=True, on_delete=models.CASCADE)

    @classmethod
    def get_sessions(cls):
        sessions = cls.objects.filter(Availability=True)
        return sessions

    @classmethod
    def get_booked_sessions(cls):
        sessions = cls.objects.filter(Availability=False)
        return sessions

class Inpatient(models.Model):
    Availability = models.BooleanField(default=True)
    starting_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User,null =True,blank=True, on_delete=models.CASCADE)


    @classmethod
    def get_vacancies(cls):
        vacancies = cls.objects.filter(Availability=True)
        return vacancies

    @classmethod
    def get_booked_vacancies(cls):
        vacancies = cls.objects.filter(Availability=False)
        return vacancies
class Reservations(models.Model):
    patient_type =  models.CharField(max_length=200,null=True, blank=True)
    user = models.ForeignKey(User)
