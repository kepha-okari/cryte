from django.shortcuts import render,redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .config import username1, apikey1
from .models import Profile, Question, Comment, Session, Inpatient, Record, Appointment, Reservations
from .forms import ProfileForm, QuestionForm, CommentForm, RecordForm
from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

from wsgiref.util import FileWrapper
import mimetypes
from django.conf import settings
import os

@login_required(login_url='/accounts/login')
def index(request):
    title = 'BADILI'
    current_user = request.user
    if_profile = Profile.objects.filter(user = current_user.id).count()

    if if_profile == 0:
        profile = Profile.objects.update_or_create(
        user = current_user,
        defaults={
            'last_name' : 'Not yet set',
            'phone_number' : 0,
            'addiction' :'Not yet set',
            'email' : 'default@mail.com'
            })
    else:
        profile = Profile.objects.get(user = current_user.id)
        user_type = profile.user_type
    return render(request, 'index.html', { "title": title, "profile": profile,"user_type":user_type})

def choose(request):
    title = 'BADILI'
    current_user = request.user
    profile = Profile.objects.get(user_id = current_user.id)
    return render(request, 'choose.html', { "title": title, "profile": profile})



@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    requested_profile = Profile.objects.get(user = current_user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            requested_profile.first_name = form.cleaned_data['first_name']
            requested_profile.last_name = form.cleaned_data['last_name']
            requested_profile.email = form.cleaned_data['email']
            requested_profile.phone_number = '0'+str(form.cleaned_data['phone_number'])
            requested_profile.addiction = form.cleaned_data['addiction']
            requested_profile.save()
            return redirect('bookings')
        else:
            print('form  is invalid')
    else:
        form = ProfileForm()
    return render(request, 'profile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def view_profile(request,user_id):
    title = 'BADILI'
    profile = Profile.get_profile(user_id)
    return render(request, 'view-profile.html', {"title": title, "profile":profile})


@login_required(login_url='/accounts/login/')
def post_question(request):
    current_user = request.user
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            opinion = form.save(commit = False)
            opinion.user = current_user
            opinion.save()
        return redirect(index)
    else:
        form = QuestionForm()
    return render(request, 'question.html', {"form": form, "current_user":current_user})

@login_required(login_url='/accounts/login/')
def save_record(request):
    current_user = request.user
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit = False)
            record.user = current_user
            record.Recurrent = True
            record.save()

        return redirect('Choose')
    else:
        form = RecordForm()
    return render(request, 'record.html', {"form": form})

def view_records(request):
    title = 'BADILI'
    records = Record.get_records
    return render(request, 'view-records.html', {"title": title, "records":records})



@login_required(login_url='/accounts/login/')
def post_comment(request, q_id):
    current_question = Question.get_specific_question(q_id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.user = current_user
            comment.question = current_question
            comment.save()
        return redirect(single_question,current_question.id)
    else:
        form = CommentForm()
    return render(request, 'comment.html', {"form": form,"current_question":current_question})


@login_required(login_url='/accounts/login/')
def all_questions(request):
    title = 'BADILI'
    questions = Question.get_questions
    return render(request, 'all-questions.html', {"title": title, "questions":questions})


@login_required(login_url='/accounts/login/')
def single_question(request,question_id):
    title = 'BADILI'
    comments = Comment.objects.filter(question=question_id)
    question = Question.objects.get(id=question_id)
    return render(request, 'single-question.html', {"title": title, "question":question, "comments":comments})


@login_required(login_url='/accounts/login/')
def unbooked_session(request):
    title = 'BADILI'
    current_user = request.user
    current_profile = Profile.objects.get(user_id = current_user.id )
    if current_profile.last_name == 'Not yet set':
        return redirect('Profile')
    else:
        sessions = Session.get_sessions
    return render(request, 'booking.html', { "title": title, "sessions":sessions})

@login_required(login_url='/accounts/login/')
def unbooked_vacancies(request):
    title = 'BADILI'
    current_user = request.user
    current_profile = Profile.objects.get(user_id = current_user.id )
    if current_profile.last_name == 'Not yet set':
        return redirect('Profile')
    else:
        vacancies = Inpatient.get_vacancies
    return render(request, 'inpatient.html', { "title": title, "vacancies":vacancies})


@login_required(login_url='/accounts/login/')
def reserve_session(request,session_id):
    title = 'BADILI'
    profile = Profile.get_profile(request.user.id)
    user_contact = profile.phone_number
    sessions = Session.get_sessions
    session = Session.objects.get(id = session_id)
    session.Availability = False
    session.user = request.user
    session.save()

    when = session.sloted_date


    # send confirmation message to the user
    username = username1
    apikey = apikey1

    to = user_contact
    message = 'Congratulations '+ request.user.username.upper() +' for making an effort to transform.\n' 'Your have reserved a session with iRehab on '+ str(when)[:10] + ' at ' + str(when)[11:16]


    gateway = AfricasTalkingGateway(username, apikey)

    try:
        # Thats it, hit send and we'll take care of the rest.

        results = gateway.sendMessage(to, message)

        for recipient in results:
            # status is either "Success" or "error message"
            print('number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                recipient['status'],
                                                                recipient['messageId'],
                                                                recipient['cost']))

    except AfricasTalkingGatewayException as e:
        print('Encountered an error while sending: %s' % str(e))

    #
    # #     # return HttpResponse(response, content_type='text/plain')
    #

    return redirect('bookings')


@login_required(login_url='/accounts/login/')
def inpatient_reservation(request,inpatient_id):
    title = 'BADILI'
    profile = Profile.get_profile(request.user.id)
    user_contact = profile.phone_number
    vacancies = Inpatient.get_vacancies
    vacancy = Inpatient.objects.get(id = inpatient_id)
    vacancy.Availability = False
    vacancy.save()

    starting = vacancy.starting_date
    ending = vacancy.finish_date

    # send confirmation message to the user
    username = username1
    apikey = apikey1

    to = user_contact
    message = 'Congratulations '+ request.user.username.upper() +'.\n' 'You have reserved a slot at iRehab from '+ str(starting)[:10] + ' to ' + str(ending)[:10] +' for in-patient services'

    gateway = AfricasTalkingGateway(username, apikey)

    try:
        # Thats it, hit send and we'll take care of the rest.

        results = gateway.sendMessage(to, message)

        for recipient in results:
            # status is either "Success" or "error message"
            print('number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                recipient['status'],
                                                                recipient['messageId'],
                                                                recipient['cost']))

    except AfricasTalkingGatewayException as e:
        print('Encountered an error while sending: %s' % str(e))

    return redirect('bookings')

#
# def message(request):
#         title = 'BADILI'
#         username = 'Nanda'
#         apikey = 'ccd6a5c49876e24e7408a7f2d5f8d6e04a3a8d56f00d9920874ec94ff656d36b'
#
#         to = '0712567583'
#         message = 'This is I rehab Welcome message '
#
#         gateway = AfricasTalkingGateway(username, apikey)
#
#         try:
#             # Thats it, hit send and we'll take care of the rest.
#
#             results = gateway.sendMessage(to, message)
#
#             for recipient in results:
#                 # status is either "Success" or "error message"
#                 print('number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
#                                                                     recipient['status'],
#                                                                     recipient['messageId'],
#                                                                     recipient['cost']))
#
#         except AfricasTalkingGatewayException as e:
#             print('Encountered an error while sending: %s' % str(e))
#
#         # return HttpResponse(response, content_type='text/plain')
#
#         return render(request, 'index.html', { "title": title})


@login_required(login_url='/accounts/login')
def view_outpatient(request):
    title = 'BADILI'
    current_user = request.user
    reservations = Session.get_booked_sessions
    return render(request, 'view-out-booked.html', { "title": title,  "reservations": reservations})

@login_required(login_url='/accounts/login')
def view_inpatient(request):
    title = 'BADILI'
    current_user = request.user
    reservations = Inpatient.get_booked_vacancies
    return render(request, 'view-in-booked.html', { "title": title,  "reservations": reservations})

def view_test(request):
    current_user = request.user
    Profile.objects.update_or_create(
    first_name=current_user.username,
    user_id = current_user.id,
    defaults={
        'last_name' : 'Not yet set',
        'phone_number' : 0,
        'addiction' :'Not yet set',
        'email' : 'default@mail.com'
        })
    return render(request,'test.html')
