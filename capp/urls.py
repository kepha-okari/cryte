from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$',views.index, name='bookings'),
    url(r'^question/', views.post_question, name='PostQuestion'),
    url(r'^all/questions/', views.all_questions, name='AllQuestions'),
    url(r'^single/question/(\d+)', views.single_question, name='SingleQuestion'),
    url(r'^comment/(\d+)', views.post_comment, name='Comment'),
    url(r'^view/booking/', views.unbooked_session, name='ViewSessions'),
    url(r'^view/slots/', views.unbooked_vacancies, name='ViewSlots'),
    url(r'^view/reserve/outpatient(\d+)', views.reserve_session, name='Reserve'),
    url(r'^view/reserve/inpatient(\d+)', views.inpatient_reservation, name='ReserveInpatient'),
    url(r'^save/record/', views.save_record, name='SaveRecord'),
    url(r'^view/records/', views.view_records, name='ViewRecord'),
    url(r'^save/profile/', views.profile, name='Profile'),
    url(r'^view/profile/(\d+)', views.view_profile, name='ViewProfile'),
    url(r'^view/outpatient/bookings/', views.view_outpatient, name='OutBook'),
    url(r'^view/inpatient/bookings/', views.view_inpatient, name='InBook'),
    url(r'^choose/service', views.choose, name='Choose'),
    url(r'^test/', views.view_test, name='Test'), # this is just a test url

    # url(r'^view/message/', views.message, name='Message'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

]
