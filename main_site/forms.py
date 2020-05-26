from django import forms
from .models import LabSession, Request, Question, tempStoreUserLocationLink, Topic

def queryset_to_choice(qs, extra):
    res = [(-1, 'All')]
    for row in qs:
        res.append((row.pk, str(row)))
    res.append(extra)
    return tuple(res)

    
# Select Lab session
class SelectLabForm(forms.ModelForm):
    class Meta:
        model = tempStoreUserLocationLink
        fields = ['lab_session']

# Choose from set of requests
class SelectRequest(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["request_location"] #this may not be needed

# Submit request status update
class StatusUpdateForm(forms.Form):
    pass

# Ask question
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ["request"] # field names required for form

    def clean_question_text(self):
        # Append profanities to blacklist
        blacklist = []
        badWords = open("profanities.txt", "r")
        line = badWords.readline()
        while line:
            word = line.strip(" \n")
            blacklist.append(word)
            line = badWords.readline()
        badWords.close()
      
        # Check if input contains any of the profanities     
        question_text = self.cleaned_data['question_text']
        for profanity in blacklist:
            if (len(profanity) == 0): continue
            if profanity in question_text.lower():
                raise forms.ValidationError("No profanities!")
        return question_text


class FilterTopicForm(forms.Form):
    topic = forms.ChoiceField(choices=queryset_to_choice(Topic.objects.all(), (-2, 'Mark')))


# ADMIN/DEMO forms
class NewTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["topic_text"]

class NewLabSession(forms.ModelForm):
    class Meta:
        model = LabSession
        fields = ["lab_session"]