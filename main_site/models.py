from django.db import models

# Create your models here.
class Person(models.Model):
    username = models.CharField(max_length=8)

    def __str__(self):
        return self.username


class LabSession(models.Model):
    lab_session = models.CharField(max_length=30)

    def __str__(self):
        return self.lab_session


class Request(models.Model):
    lab_session = models.ForeignKey(LabSession, on_delete=models.CASCADE)
    request_location = models.CharField(max_length=30)
    request_made = models.TimeField(auto_now=True)
    request_start = models.TimeField(default=None, null=True, blank=True)
    request_end = models.TimeField(default=None, null=True, blank=True)
    status = models.CharField(default='Not started', choices=(('Waiting Question', 'Waiting Question'), ('Not started', 'Not started'), ('Help needed', 'Help needed'), ('Gave up', 'Gave up'), ('Complete', 'Complete'), ('Serviced', 'Serviced'), ('Time out', 'Time out')), max_length=20)

    def __str__(self):
        return str(self.lab_session) + ': ' + self.request_location + ' - made at ' + str(self.request_made)


class Topic(models.Model):
    topic_text = models.CharField(max_length=30)
    def __str__(self):
        return self.topic_text


class Question(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=30)

    def __str__(self):
        return str(self.topic) + ': ' + self.question_text


class RequestHandler(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.person) + ' ' + str(self.request)


class tempStoreUserLocationLink(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    lab_session = models.ForeignKey(LabSession, on_delete=models.CASCADE)

    def __str__(self):
        if self.person:
            return str(self.person) + ' ' + str(self.lab_session)
        return str(self.location) + ' ' + str(self.lab_session)

