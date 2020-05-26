from django.test import TestCase, Client
from django.urls import reverse
from main_site.models import Person, LabSession, Request, Topic, Question, RequestHandler, tempStoreUserLocationLink
from main_site.views import *
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.person_url = reverse('portal')
        self.person1_url = reverse('about')
        self.person2_url = reverse('select_lab')
        self.person3_url = reverse('select_lab_ta')
        self.person4_url = reverse('select_student_filtered', args=[1])
        self.person5_url = reverse('select_student')
        self.person6_url = reverse('service_request')
        self.person7_url = reverse('logout')
        self.person8_url = reverse('logout_success')
        self.person9_url = reverse('stats')
        self.person10_url = reverse('stats_filtered', args=['11120'])
        self.person11_url = reverse('graph')
        self.person12_url = reverse('error_mobile')
        self.person13_url = reverse('select_lab_student')
        self.person14_url = reverse('question_or_mark')
        self.person15_url = reverse('ask_question')
        self.person16_url = reverse('waiting')
        self.person17_url = reverse('select_lab_student')
        self.person18_url = reverse('demo_home')
        self.person19_url = reverse('drop')
        self.person20_url = reverse('setup')
        self.person21_url = reverse('new_user')
        self.person22_url = reverse('new_topic')
        self.person23_url = reverse('new_lab')

    def test_1_GET(self):
            response = self.client.get(self.person_url)
            self.assertEquals(response.status_code, 200)

    def test_2_GET(self):
            response = self.client.get(self.person1_url)
            self.assertEquals(response.status_code, 200)
        
    def test_3_GET(self):
            response = self.client.get(self.person2_url)
            self.assertEquals(response.status_code, 302)
    
    def test_4_GET(self):
            response = self.client.get(self.person3_url)
            self.assertEquals(response.status_code, 302)
    
    def test_5_GET(self):
            response = self.client.get(self.person4_url)
            self.assertEquals(response.status_code, 302)
    
    def test_6_GET(self):
            response = self.client.get(self.person5_url)
            self.assertEquals(response.status_code, 302)
    
    def test_7_GET(self):
            response = self.client.get(self.person6_url)
            self.assertEquals(response.status_code, 302)
    
    def test_8_GET(self):
            response = self.client.get(self.person7_url)
            self.assertEquals(response.status_code, 302)
    
    def test_9_GET(self):
            response = self.client.get(self.person8_url)
            self.assertEquals(response.status_code, 200)
    
    def test_10_GET(self):
            response = self.client.get(self.person9_url)
            self.assertEquals(response.status_code, 302)
    
    def test_11_GET(self):
            response = self.client.get(self.person10_url)
            self.assertEquals(response.status_code, 302)
    
    def test_12_GET(self):
            response = self.client.get(self.person11_url)
            self.assertEquals(response.status_code, 200)
    
    def test_13_GET(self):
            response = self.client.get(self.person12_url)
            self.assertEquals(response.status_code, 302)
    
    def test_14_GET(self):
            response = self.client.get(self.person13_url)
            self.assertEquals(response.status_code, 200)
    
    def test_15_GET(self):
            response = self.client.get(self.person14_url)
            self.assertEquals(response.status_code, 200)
    
    def test_16_GET(self):
            response = self.client.get(self.person15_url)
            self.assertEquals(response.status_code, 302)
    
    def test_17_GET(self):
            response = self.client.get(self.person16_url)
            self.assertEquals(response.status_code, 302)
    
    def test_18_GET(self):
            response = self.client.get(self.person17_url)
            self.assertEquals(response.status_code, 200)
    
    def test_19_GET(self):
            response = self.client.get(self.person18_url)
            self.assertEquals(response.status_code, 302)

    def test_20_GET(self):
            response = self.client.get(self.person19_url)
            self.assertEquals(response.status_code, 302)
    
    def test_21_GET(self):
            response = self.client.get(self.person20_url)
            self.assertEquals(response.status_code, 302)

    def test_22_GET(self):
            response = self.client.get(self.person21_url)
            self.assertEquals(response.status_code, 302)

    def test_23_GET(self):
            response = self.client.get(self.person22_url)
            self.assertEquals(response.status_code, 302)

    def test_24_GET(self):
            response = self.client.get(self.person23_url)
            self.assertEquals(response.status_code, 302)


    def test_selectLabSessionSTUDENTView_POST(self):
            person1 = Person.objects.create(username = 'hello')
            labsesh1 = LabSession.objects.create(lab_session = 'tootil1')
            tempStoreUserLocationLink.objects.create(person = person1, location = 'tootil0', lab_session = labsesh1)
            response = self.client.post(self.person_url, {
                'lab_session': labsesh1
            })
            self.assertEquals(response.status_code, 200)

    def test_selectLabSessionTAView_POST(self):
            person1 = Person.objects.create(username = 'hello')
            labsesh1 = LabSession.objects.create(lab_session = 'tootil1')
            tempStoreUserLocationLink.objects.create(person = person1, location = 'tootil0', lab_session = labsesh1)
            user = tempStoreUserLocationLink.objects.get(lab_session = labsesh1).pk
            response = self.client.post(self.person1_url, {
                'lab_session': labsesh1
            })
            self.assertEquals(response.status_code, 200)