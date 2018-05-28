from django.contrib import admin
from .models import Profile, Question, Comment, Session, Record, Doctor, Inpatient

# Register your models here.

admin.site.register(Inpatient)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Session)
admin.site.register(Record)
admin.site.register(Doctor)
