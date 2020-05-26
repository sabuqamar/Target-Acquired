from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
import socket, os



import random
import string
from datetime import datetime, timedelta



from .forms import *
from .models import *

# Util functions
def getPerson(request):
    username = request.user.username
    if request.user.is_authenticated:
        if Person.objects.filter(username=username).exists():
            return Person.objects.get(username=username)
        p = Person(username=username)
        p.save()
        return p

def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists()

def is_demo_user(user):
    print('************************')
    print(user.groups.filter(name='demo').exists())
    return user.groups.filter(name='demo').exists()

def isPersonBusy(request):
    person = getPerson(request)
    if RequestHandler.objects.filter(person=person).exists():
        return True
    return False

def getLocation(request):
    if not request.user_agent.is_mobile:
    # source url: https://stackoverflow.com/questions/23329743/django-remote-host-empty-answer
    # Author: rak007
    # Accessed: 10/03/2020
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
            regip = real_ip.split(",")[0]
        except:
            try:
                regip = request.META['REMOTE_ADDR']
            except:
                regip = ""
        if(regip == "127.0.0.1"):
            myHost=socket.gethostname()
        else:
            try:
                resultHost = socket.gethostbyaddr(regip)
            except socket.herror:
                resultHost=['PC']
            myHost=resultHost[0]
        # End reference
        return myHost.split('.')[0]
    else:
        return 'Mobile'
def makeStudentCards(lab_session, topic_filter=-1):
    mark_only = False
    if topic_filter == -2:
        mark_only = True
    if topic_filter > -1:
        topic = Topic.objects.get(id=topic_filter)

    students_waiting = Request.objects.filter(status__in=['help needed', 'Not started'])
    students_in_lab = tempStoreUserLocationLink.objects.filter(lab_session=lab_session).values('location')
    computer_locations = []
    for student in students_in_lab:
        if student['location']:
            computer_locations.append(student['location'])

    cards = [[]]
    count = 0
    for student in students_waiting:
        if not student.request_location in computer_locations:
            continue
        if count == 4:
            count = 0
            cards.append([])
        problem = ''
        colour = 'white'
        if student.status == 'help needed':
            problem = "ADDITIONAL HELP REQUIRED. "
            colour = 'red'
        if Question.objects.filter(request=student).exists():
            if mark_only:
                continue
            question = Question.objects.get(request=student)
            if topic_filter != -1:
                if question.topic != topic:
                    continue
            problem += str(question.topic) + ': ' + question.question_text
        else:
            if topic_filter == -2 or topic_filter == -1:
                problem += 'I am ready to be marked.'
            else:
                continue

        if (student.status == 'Waiting Question'): continue

        minutes_made = student.request_made.minute
        minutes_now = datetime.now().time().minute

        hour_made = student.request_made.hour
        hour_now = datetime.now().time().hour

        time_dif = (hour_now - hour_made) * 60 + minutes_now - minutes_made

        if time_dif > 150 or time_dif < 0: # 2.5 hours limit?
            student.status = 'Time out'
            student.save()
            continue

        card = {
            'location': student.request_location,
            'time' : time_dif,
            'problem': problem,
            'colour': colour,
            'pk': 'request-' + str(student.pk)
        }
        cards[-1].append(card)
        count += 1

    return cards



# Drop tables
def dropLabSessionLinks():
    objs = tempStoreUserLocationLink.objects.all()
    for obj in objs:
        obj.delete()

def dropAllRequests():
    objs = Request.objects.all()
    for obj in objs:
        obj.delete()

def dropAllUsers():
    objs = list(User.objects.all()) + list(Person.objects.all())
    for obj in objs:
        if obj.username == 'dev' or obj.username == 'demo':
            continue
        obj.delete()

def dropTopics():
    objs = Topic.objects.all()
    for obj in objs:
        obj.delete()

def dropLabSessions():
    objs = LabSession.objects.all()
    for obj in objs:
        obj.delete()


# create dummy data
def createLabSessions():
    session_codes = [
        '10120', '11120', '11212', '13212', '12111', '13212', '15111', '15212', '16321', '16421'
    ]
    for code in session_codes:
        for n in range(1, random.randint(0, 12)):
            obj = LabSession(lab_session = 'COMP%s-Lab-%d' % (code, n))
            obj.save()
    print('Lab session\'s created.')

def createTopics():
    topics = [
        'Hardware', 'PC problem', 'Bash', 'Lab script', 'Software', 'Other'
    ]
    for topic in topics:
        if not Topic.objects.filter(topic_text=topic).exists():
            Topic(topic_text=topic).save()

def createDummyUsers():
    # create 3 TA users
    usernames = ['a12346bc', 'd12346ef', 'g12346hi']
    for i in range(3):
        if not User.objects.filter(username=usernames[i]).exists():
            user = User.objects.create_user(usernames[i], '', 'ta_password')
            user.save()

    # create a lecturer
    lec_group = Group.objects.get(name='lecturer')
    if not User.objects.filter(username='z98765le').exists():
        user = User.objects.create_user('z98765le', '', 'password')
        user.save()
        lec_group.user_set.add(user)

    # create a demo super user
    demo_group = Group.objects.get(name='demo')
    if not User.objects.filter(username='demo').exists():
        user = User.objects.create_user('demo', '', 'demo')
        user.save()
        demo_group.user_set.add(user)

def createDummyData():
    createLabSessions()
    createTopics()
    createDummyUsers()

    lab_sessions = LabSession.objects.all()
    for lab in lab_sessions:
        n_add = random.randint(15, 60)
        for i in range(n_add):
            pc = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            newRequestObj = Request(lab_session=lab, request_location=pc)
            newRequestObj.save()
            newTempLocationLink = tempStoreUserLocationLink(location=pc, lab_session=lab)
            newTempLocationLink.save()
            if random.randint(0, 1) == 1:
                topic = Topic.objects.order_by('?').first()
                question = Question(request=newRequestObj, topic=topic, question_text="This is a question!")
                question.save()
    print('Success')


# Create your views here.

# # ALL USERS
def redirectLabView(request):
    if request.user.is_authenticated:
        if is_demo_user(request.user):
            return HttpResponseRedirect(reverse('demo_home'))
        else:
            return HttpResponseRedirect(reverse('select_lab_ta'))
    print('student lab')
    return HttpResponseRedirect(reverse('select_lab_student'))

# about us
def AboutUsView(request):
    return render(
        request,
        'AboutUs.html',
        {}
    )


@login_required
def selectLabSessionTAView(request):
    form = SelectLabForm() # change form
    if request.POST:
        form = SelectLabForm(request.POST)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.person = getPerson(request)
            if tempStoreUserLocationLink.objects.filter(person=lab.person).exists():
                record = tempStoreUserLocationLink.objects.get(person=lab.person)
                record.lab_session = lab.lab_session
                record.save()
            else:
                lab.save()
            return HttpResponseRedirect(reverse('select_student'))
    return render(
        request,
        'choose_lab.html',
        {'form': form}
    )


@login_required
def SelectStudentView(request, topic_filter=-1):
    topic_filter = int(topic_filter)
    if not (Topic.objects.filter(id=topic_filter).exists() or topic_filter in [-1, -2]):
        topic_filter = -1
    person = getPerson(request)
    if tempStoreUserLocationLink.objects.filter(person=person).exists():
        lab_session = tempStoreUserLocationLink.objects.get(person=person).lab_session
    else:
        return HttpResponseRedirect(reverse('select_lab_ta'))

    if isPersonBusy(request):
        return HttpResponseRedirect(reverse('service_request'))

    cards = (makeStudentCards(lab_session, int(topic_filter)))
    form = FilterTopicForm()
    if request.POST:
        pk = -1
        for var in request.POST:
            if 'request-' in var:
                pk = int(var.replace('request-', ''))
            if var == 'filter':
                form = FilterTopicForm(request.POST)
                if form.is_valid():
                    return HttpResponseRedirect(reverse('select_student_filtered', kwargs={'topic_filter': int(form.cleaned_data['topic'])}))
        if pk > -1:
            requestObj = Request.objects.get(pk=pk)
            requestObj.request_start = datetime.now()
            requestObj.status = 'Serviced'
            requestObj.save()
            RequestHandler.objects.create(person=person, request = requestObj)
            return HttpResponseRedirect(reverse('service_request'))

    return render(
        request,
        'staff/select_student.html',
        {'students': cards, 'form': FilterTopicForm}
    )


@login_required
def ServiceRequestView(request):
    person = getPerson(request)
    if RequestHandler.objects.filter(person=person).exists():
        rq_handler = RequestHandler.objects.get(person=person)
        rq = rq_handler.request
    else:
        return HttpResponseRedirect(reverse('select_student'))

    if rq.status == "Complete":
        return HttpResponseRedirect(reverse('select_student'))

    if request.POST:
        for var in request.POST:
            if var == 'complete':
                rq.request_end = datetime.now()
                rq.status = 'Complete'
            elif var == 'help':
                rq.status = 'help needed'
            elif var == 'give_up':
                rq.status = 'Gave up'
            else:
                continue
            rq_handler.delete()
            rq.save()
            return HttpResponseRedirect(reverse('select_student'))

    if Question.objects.filter(request=rq).exists():
        question = Question.objects.get(request=rq)
        problem = str(question.topic) + ': ' + question.question_text
    else:
        problem = 'I am ready to be marked.'

    return render(
        request,
        'staff/service_request.html',
        {'student': rq, 'problem': problem}
    )



@login_required
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout_success'))

def LogoutSuccessView(request):
    return render(
        request,
        'staff/logout.html', # replace with correct webpage
        {}
    )

# LECTURER ONLY
@login_required
@user_passes_test(lambda u: is_lecturer(u))
def StatisticsView(request):
    return HttpResponse("StatisticsView")

# STUDENT
def errorMobileView(request, next_url='select_lab_student'):
    if request.user_agent.is_mobile:
        return HttpResponse("Sorry. Mobile use is not permitted for students. Please use a lab machine")
    else:
        return HttpResponseRedirect(reverse(next_url))

def selectLabSessionSTUDENTView(request):
    if request.META.get('HTTP_REFERER') == 'https://x2.eu.pythonanywhere.com/':
        logout(request)
    if request.user_agent.is_mobile:
        return HttpResponseRedirect(reverse('error_mobile'))
    time_threshold = datetime.now() - timedelta(hours=2, minutes=30)
    currentLocation = getLocation(request)
    if tempStoreUserLocationLink.objects.filter(location=currentLocation).exists():
        if Request.objects.filter(request_location=getLocation(request), request_made__lt=time_threshold).exclude(status__in=['Gave up', 'Complete', 'Time out']).exists():
            return HttpResponseRedirect(reverse('waiting'))
    form = SelectLabForm()
    if request.POST:
        form = SelectLabForm(request.POST)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.location = getLocation(request)
            if tempStoreUserLocationLink.objects.filter(location=lab.location).exists():
                record = tempStoreUserLocationLink.objects.get(location=lab.location)
                record.lab_session = lab.lab_session
                record.save()
            else:
                lab.save()
            return HttpResponseRedirect(reverse('question_or_mark'))
    return render(
        request,
        'choose_lab.html',
        {'form': form}
    )


def SelectQuestionOrMarkView(request):
    if request.user_agent.is_mobile:
        return HttpResponseRedirect(reverse('error_mobile'))
    currentLocation = getLocation(request)
    if tempStoreUserLocationLink.objects.filter(location=currentLocation).exists():
        record = tempStoreUserLocationLink.objects.get(location=currentLocation)
    else:
        return HttpResponseRedirect(reverse('select_lab_student'))

    if Request.objects.filter(request_location=currentLocation, status__in=["Not started", "help needed"]).exists():
        return HttpResponseRedirect(reverse('waiting'))

    if request.POST:
        for var in request.POST:
            if var == 'question':
                query = Request(lab_session = record.lab_session, request_location = currentLocation)
                query.status = 'Waiting Question'
                query.save()

                return HttpResponseRedirect(reverse('ask_question'))
            elif var == 'mark':
                query = Request(lab_session = record.lab_session, request_location = currentLocation)
                query.save()

                return HttpResponseRedirect(reverse('waiting'))

    return render(
        request,
        'student/select_q_or_m.html',
        {'lab': record.lab_session.lab_session}
    )

def AskQuestionView(request):
    if request.user_agent.is_mobile:
        return HttpResponseRedirect(reverse('error_mobile'))
    currentLocation = getLocation(request)
    if tempStoreUserLocationLink.objects.filter(location=currentLocation).exists():
        record = tempStoreUserLocationLink.objects.get(location=currentLocation)
    else:
        return HttpResponseRedirect(reverse('select_lab_student'))

    form = QuestionForm()
    currentLocation = getLocation(request)
    if Request.objects.filter(request_location=currentLocation, status__in=["Not started", "help needed", 'Waiting Question']).exists():
        query = Request.objects.filter(request_location=currentLocation, status__in=['help needed', 'Not started', 'Waiting Question']).order_by('-request_made')[0]
    else:
        return HttpResponseRedirect(reverse('question_or_mark'))

    if request.POST:
        form = QuestionForm(request.POST)
        if form.is_valid():
            query.status = "Not started"
            query.save()

            a_question = form.save(commit = False)
            a_question.request = query
            a_question.save()
            return HttpResponseRedirect(reverse('waiting'))

    return render(
        request,
        'student/ask_question.html',
        {'form' : form, 'lab': record.lab_session.lab_session}
    )

def WaitView(request):
    if request.user_agent.is_mobile:
        return HttpResponseRedirect(reverse('error_mobile'))
    currentLocation = getLocation(request)
    if tempStoreUserLocationLink.objects.filter(location=currentLocation).exists():
        record = tempStoreUserLocationLink.objects.get(location=currentLocation)
        lab = record.lab_session.lab_session
    else:
        lab = 'UNKNOWN'

    queries = {'mark': {'queue': 0, 'exists': False, 'query': None}, 'q': {'queue': 0, 'topic': '', 'body': '', 'exists': False, 'query': None}}
    quit_count = 0
    if Request.objects.filter(request_location=currentLocation, status__in=["Not started", "help needed"]).exists():
        queryRes = Request.objects.filter(request_location=currentLocation,  status__in=["Not started", "help needed"])
        maxQueue = len(Request.objects.filter(lab_session=record.lab_session, status__in=['help needed', 'Not started']))
        numQuestions = len(Question.objects.filter(request__lab_session=record.lab_session, request__status__in=['help needed', 'Not started']))
        for query in queryRes:

            if query.status in ['Gave up', 'Complete', 'Time out']  or query.request_end != None:
                quit_count += 1
            if Question.objects.filter(request=query).exists():
                q = Question.objects.filter(request=query)[0]
                queries['q']['exists'] = True
                queries['q']['topic'] = q.topic
                queries['q']['body'] = q.question_text
                queries['q']['query'] = query
                queries['q']['queue'] = numQuestions - 1
            else:
                queries['mark']['exists'] = True
                queries['mark']['query'] = query
                queries['mark']['queue'] = maxQueue - numQuestions - 1
    else:
        return HttpResponseRedirect(reverse('question_or_mark'))

    if quit_count == 2:
        return HttpResponseRedirect(reverse('question_or_mark'))

    if request.POST:
        for var in request.POST:
            if var == 'cancel-mark':
                query = queries['mark']['query']
                query.status = 'cancel'
                query.save()
            elif var == 'cancel-question':
                query = queries['q']['query']
                query.status = 'cancel'
                query.save()
            elif var == 'new-mark':
                query = Request(lab_session = record.lab_session, request_location = currentLocation)
                query.save()
            elif var == 'new-question':
                query = Request(lab_session = record.lab_session, request_location = currentLocation)
                query.save()
                return HttpResponseRedirect(reverse('ask_question'))
        return HttpResponseRedirect(reverse('waiting'))

    return render(
        request,
        'student/wait.html',
        {'queries': queries, 'lab': lab}
    )


# ADMINISTRATOR ONLY
@login_required
@user_passes_test(is_demo_user, login_url='/staff', redirect_field_name=None)
def DemoDashView(request):
    return render(
        request,
        'demo/dash.html',
        {}
    )


@login_required
@user_passes_test(is_demo_user, login_url='/staff', redirect_field_name=None)
def ClearDBView(request):
    if request.POST:
        if 'yes' in request.POST:
            dropLabSessionLinks()
            dropAllRequests()
            dropAllUsers()
            dropTopics()
            dropLabSessions()
        return HttpResponseRedirect(reverse('demo_home'))
    return render(
        request,
        'demo/button.html',
        {'title': 'Clear the database'}
    )

@login_required
@user_passes_test(is_demo_user, login_url='/staff', redirect_field_name=None)
def SetupDBView(request):
    if request.POST:
        if 'yes' in request.POST:
            createDummyData()
        return HttpResponseRedirect(reverse('demo_home'))
    return render(
        request,
        'demo/button.html',
        {'title': 'Setup the database'}
    )

@login_required
@user_passes_test(is_demo_user, login_url='/staff', redirect_field_name=None)
def NewUserView(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    return render(
        request,
        'demo/form.html',
        {'form': form}
    )

@login_required
@user_passes_test(is_demo_user, login_url='/staff', redirect_field_name=None)
def NewTopicView(request):
    form = NewTopicForm()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            form.save()
    return render(
        request,
        'demo/form.html',
        {'form': form}
    )

@login_required
@user_passes_test(is_demo_user, login_url='/staff', redirect_field_name=None)
def NewLabSessionView(request):
    form = NewLabSession()
    if request.method == 'POST':
        form = NewLabSession(request.POST)
        if form.is_valid():
            form.save()
    return render(
        request,
        'demo/form.html',
        {'form': form}
    )


