from django import forms

class RecommendForm(forms.Form):
   user_vanity = forms.CharField(max_length = 100, required=False)
   user_id = forms.CharField(max_length = 100, required=False)