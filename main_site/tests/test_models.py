from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from main_site.models import Person, LabSession, Request, Topic, Question, RequestHandler, tempStoreUserLocationLink

class TestModels(TestCase):
    @classmethod
    def setUpTestData(self):
        person1 = Person.objects.create(username = 'hello')
        person2 = Person.objects.create(username = '')
        labsesh1 = LabSession.objects.create(lab_session = 'tootil1')
        request1 = Request.objects.create(lab_session = labsesh1, request_location = 'lf31')
        request2 = Request.objects.create(lab_session = labsesh1, request_location = 'lf31', request_start = timezone.now(), request_end = timezone.now())
        topic1 = Topic.objects.create(topic_text = 'randomtopic')
        Question.objects.create(request = request1, topic = topic1, question_text = 'what is life')
        RequestHandler.objects.create(person = person1, request = request1)
        tempStoreUserLocationLink.objects.create(person = person1, location = 'tootil0', lab_session = labsesh1)
        tempStoreUserLocationLink.objects.create(lab_session = labsesh1)
        tempStoreUserLocationLink.objects.create(person = person2, location = '', lab_session = labsesh1)
##################### Person class #######################
    def test_person_username_max_length(self):
        user = Person.objects.get(id=1)
        max_length = user._meta.get_field('username').max_length
        self.assertEquals(max_length, 8)

    def test_person_username_label(self):
        user = Person.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')

    def test_person_is_username(self):
        user = Person.objects.get(id=1)
        expected_object_name = user.username
        self.assertEquals(expected_object_name, str(user))

##################### LabSession class #######################
    def test_LabSession_variables_max_length(self):
        user = LabSession.objects.get(id=1)
        max_length = user._meta.get_field('lab_session').max_length
        self.assertEquals(max_length, 30)


    def test_LabSession_labels(self):
        user = LabSession.objects.get(id=1)
        field_label1 = user._meta.get_field('lab_session').verbose_name
        self.assertEquals(field_label1, 'lab session')

    def test_LabSession_is_lab_session(self):
        user = LabSession.objects.get(id=1)
        expected_object_name = user.lab_session
        self.assertEquals(expected_object_name, str(user))
    
##################### Request class #######################
# check the on_delete thing
    def test_request_max_length(self):
        user = Request.objects.get(id=1)
        max_length = user._meta.get_field('request_location').max_length
        max_length1 = user._meta.get_field('status').max_length
        self.assertEquals(max_length, 30)
        self.assertEquals(max_length1, 20)

    def test_request_label(self):
        user = Request.objects.get(id=1)
        field_label = user._meta.get_field('request_location').verbose_name
        field_label1 = user._meta.get_field('status').verbose_name
        field_label2 = user._meta.get_field('lab_session').verbose_name
        field_label3 = user._meta.get_field('request_made').verbose_name
        field_label4 = user._meta.get_field('request_start').verbose_name
        field_label5 = user._meta.get_field('request_end').verbose_name
        self.assertEquals(field_label, 'request location')
        self.assertEquals(field_label1, 'status')
        self.assertEquals(field_label2, 'lab session')
        self.assertEquals(field_label3, 'request made')
        self.assertEquals(field_label4, 'request start')
        self.assertEquals(field_label5, 'request end')


    def test_request_is_lab_and_request(self):
        user = Request.objects.get(id=1)
        user1 = Request.objects.get(id=2)
        expected_object_name = str(user.lab_session) + ': ' + user.request_location + ' - made at ' + str(user.request_made)
        expected_object_name1 = str(user1.lab_session) + ': ' + user1.request_location + ' - made at ' + str(user1.request_made)
        expected_status = str(user.status)
        expected_request_start = user.request_start
        expected_request_end = user.request_end
        expected_request_made = user.request_made
        self.assertEquals(expected_object_name, str(user))
        self.assertEquals(expected_object_name1, str(user1))
        self.assertEquals(expected_status, 'Not started')
        self.assertEquals(expected_request_start, None)
        self.assertEquals(expected_request_end, None)
        # self.assertEquals(expected_request_made, timezone.now())


##################### Topic class #######################
    def test_topic_text_max_length(self):
        user = Topic.objects.get(id=1)
        max_length = user._meta.get_field('topic_text').max_length
        self.assertEquals(max_length, 30)

    def test_topic_text_label(self):
        user = Topic.objects.get(id=1)
        field_label = user._meta.get_field('topic_text').verbose_name
        self.assertEquals(field_label, 'topic text')

    def test_topic_is_topic_text(self):
        user = Topic.objects.get(id=1)
        expected_object_name = user.topic_text
        self.assertEquals(expected_object_name, str(user))
            
##################### Question class #######################
# on_delete testing
    def test_question_max_length(self):
        user = Question.objects.get(id=1)
        max_length = user._meta.get_field('question_text').max_length
        self.assertEquals(max_length, 30)

    def test_question_label(self):
        user = Question.objects.get(id=1)
        field_label = user._meta.get_field('request').verbose_name
        field_label1 = user._meta.get_field('topic').verbose_name
        field_label2 = user._meta.get_field('question_text').verbose_name
        self.assertEquals(field_label, 'request')
        self.assertEquals(field_label1, 'topic')
        self.assertEquals(field_label2, 'question text')

    def test_question_is_topic_and_question(self):
        user = Question.objects.get(id=1)
        expected_object_name = str(user.topic) + ': ' + str(user.question_text)
        self.assertEquals(expected_object_name, str(user))
    
##################### RequestHandler class #######################
# on_delete testing
    def test_person_username_label(self):
        user = RequestHandler.objects.get(id=1)
        field_label = user._meta.get_field('person').verbose_name
        field_label1 = user._meta.get_field('request').verbose_name
        self.assertEquals(field_label, 'person')
        self.assertEquals(field_label1, 'request')

    def test_person_is_username(self):
        user = RequestHandler.objects.get(id=1)
        expected_object_name = str(user.person) + ' ' + str(user.request)
        self.assertEquals(expected_object_name, str(user))
    
##################### tempStoreUserLocationLink class #######################
# on_delete testing
    def test_tempStoreUserLocationLink_max_length(self):
        user = tempStoreUserLocationLink.objects.get(id=1)
        max_length = user._meta.get_field('location').max_length
        self.assertEquals(max_length, 30)

    def test_temp_label(self):
        user = tempStoreUserLocationLink.objects.get(id=1)
        field_label = user._meta.get_field('person').verbose_name
        field_label1 = user._meta.get_field('location').verbose_name
        field_label2 = user._meta.get_field('lab_session').verbose_name
        self.assertEquals(field_label, 'person')
        self.assertEquals(field_label1, 'location')
        self.assertEquals(field_label2, 'lab session')

    def test_temp_with_person_with_location(self):
        user = tempStoreUserLocationLink.objects.get(id=1)
        expected_object_name = str(user.person) + ' ' + str(user.lab_session)
        self.assertEquals(expected_object_name, str(user))

    def test_temp_null_person_and_null_location(self):
        user = tempStoreUserLocationLink.objects.get(id=2)
        expected_object_name = str(user.location) + ' ' + str(user.lab_session)
        self.assertEquals(expected_object_name, str(user))

    def test_temp_blank_person_and_blank_location(self):
        user = tempStoreUserLocationLink.objects.get(id=3)
        expected_object_name = str(user.person) + ' ' + str(user.lab_session)
        self.assertEquals(expected_object_name, str(user))