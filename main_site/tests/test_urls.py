from django.test import SimpleTestCase
from django.urls import reverse, resolve 
from main_site.views import redirectLabView, AboutUsView, selectLabSessionTAView, WaitView, AskQuestionView, SelectQuestionOrMarkView, ServiceRequestView, selectLabSessionSTUDENTView, SelectStudentView, LogoutView, LogoutSuccessView, GraphView, StatisticsView, errorMobileView, DemoDashView, ClearDBView, SetupDBView, NewUserView, NewTopicView, NewLabSessionView
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    def test_portal_url_is_resolved(self):
        url = reverse('portal')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_about_us_url_is_resolved(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func, AboutUsView)

    def test_select_lab_url_is_resolved(self):
        url = reverse('select_lab')
        self.assertEquals(resolve(url).func, redirectLabView)

    def test_select_lab_ta_url_is_resolved(self):
        url = reverse('select_lab_ta')
        self.assertEquals(resolve(url).func, selectLabSessionTAView)

    def test_select_student_url_is_resolved(self):
        url = reverse('select_student_filtered', args=[1])
        self.assertEquals(url, '/staff/select/1/')

    def test_select_student2_url_is_resolved(self):
        url = reverse('select_student')
        self.assertEquals(url, '/staff/select/')

    def test_service_request_url_is_resolved(self):
        url = reverse('service_request')
        self.assertEquals(resolve(url).func, ServiceRequestView)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, LogoutView)

    def test_logout_successful_url_is_resolved(self):
        url = reverse('logout_success')
        self.assertEquals(resolve(url).func, LogoutSuccessView)

    def test_stats_url_is_resolved(self):
        url = reverse('stats')
        self.assertEquals(resolve(url).func, StatisticsView)

    def test_logout_successful_url_is_resolved(self):
        url = reverse('stats_filtered')
        self.assertEquals(resolve(url).func, StatisticsView)

    def test_logout_successful_url_is_resolved(self):
        url = reverse('graph')
        self.assertEquals(resolve(url).func, GraphView)
    
    def test_select_lab_student_url_is_resolved(self):
        url = reverse('error_mobile')
        self.assertEquals(resolve(url).func, errorMobileView)

    def test_select_lab_student_url_is_resolved(self):
        url = reverse('select_lab_student')
        self.assertEquals(resolve(url).func, selectLabSessionSTUDENTView)

    def test_question_or_mark_url_is_resolved(self):
        url = reverse('question_or_mark')
        self.assertEquals(resolve(url).func, SelectQuestionOrMarkView)

    def test_ask_question_url_is_resolved(self):
        url = reverse('ask_question')
        self.assertEquals(resolve(url).func, AskQuestionView)

    def test_waiting_url_is_resolved(self):
        url = reverse('waiting')
        self.assertEquals(resolve(url).func, WaitView)

    def test_demo_home_url_is_resolved(self):
        url = reverse('demo_home')
        self.assertEquals(resolve(url).func, DemoDashView)
    
    def test_drop_url_is_resolved(self):
        url = reverse('drop')
        self.assertEquals(resolve(url).func, ClearDBView)

    def test_setup_url_is_resolved(self):
        url = reverse('setup')
        self.assertEquals(resolve(url).func, SetupDBView)

    def test_new_user_url_is_resolved(self):
        url = reverse('new_user')
        self.assertEquals(resolve(url).func, NewUserView)
    
    def test_new_topic_url_is_resolved(self):
        url = reverse('new_topic')
        self.assertEquals(resolve(url).func, NewTopicView)
    
    def test_new_lab_url_is_resolved(self):
        url = reverse('new_lab')
        self.assertEquals(resolve(url).func, NewLabSessionView)
   
    