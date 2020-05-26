from django.test import TestCase
from main_site.forms import SelectLabForm, SelectRequest, StatusUpdateForm, QuestionForm, FilterTopicForm, SelectCourse, NewTopicForm, NewLabSession 
from main_site.models import LabSession, Request, Topic

class TestForms(TestCase):
 
    def test_SelectLabForm_form_valid_data(self):
        LabSession.objects.create(lab_session = 'tootil1')
        user = LabSession.objects.get(lab_session = 'tootil1').pk
        form = SelectLabForm(data={
            'lab_session': user
        })
        self.assertTrue(form.is_valid())

    def test_SelectLabForm_form_no_data(self):
        form = SelectLabForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
    
    def test_SelectRequest_form_valid_data(self):
        form = SelectRequest(data={
            'request_location': 'user'
        })
        self.assertTrue(form.is_valid()) 

    def test_SelectRequest_form_no_data(self):
        form = SelectRequest(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_StatusUpdateForm_form_no_data(self):
        form = StatusUpdateForm(data={})
        self.assertTrue(form.is_valid())

    def test_QuestionForm_form_valid_data(self):
        Topic.objects.create(topic_text = 'tootil1')
        user = Topic.objects.get(topic_text = 'tootil1').pk
        form = QuestionForm(data={
            'topic': user,
            'question_text': 'user'
        })
        self.assertTrue(form.is_valid())
    
    def test_QuestionForm_form_not_valid_data(self):
        Topic.objects.create(topic_text = 'tootil1')
        user = Topic.objects.get(topic_text = 'tootil1').pk
        form = QuestionForm(data={
            'topic': user,
            'question_text': 'HELL'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_QuestionForm_form_no_data(self):
        form = QuestionForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_FilterTopicForm_form_valid_data(self):
        form = FilterTopicForm(data={
            'topic': -1
        })
        self.assertTrue(form.is_valid())

    def test_FilterTopicForm_form_no_data(self):
        form = FilterTopicForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_SelectCourse_form_valid_data(self):
        form = SelectCourse(data={
            'course': 'COMP11212'
        })
        self.assertTrue(form.is_valid())

    def test_SelectCourse_form_no_data(self):
        form = SelectCourse(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_NewTopicForm_form_valid_data(self):
        form = NewTopicForm(data={
            'topic_text': "hello"
        })
        self.assertTrue(form.is_valid())

    def test_NewTopicForm_form_no_data(self):
        form = NewTopicForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_NewLabSession_form_valid_data(self):
        form = NewLabSession(data={
            'lab_session': "arch"
        })
        self.assertTrue(form.is_valid())

    def test_NewLabSession_form_no_data(self):
        form = NewLabSession(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)