from django import forms


class SubmitLyricsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    title = forms.CharField(max_length=100)
    writer = forms.CharField()
    date = forms.DateField()
    lyrics = forms.CharField()
