from django import forms

class TeamRegisterForm(forms.Form):
    team_name = forms.CharField(label='Team Name', max_length=250,widget=forms.TextInput(attrs={"class":"form-control"}))
    team_manager = forms.CharField(label='Team Manager', max_length=250,widget=forms.TextInput(attrs={"class":"form-control"}))
    team_coach = forms.CharField(label='Team Coach', max_length=250,widget=forms.TextInput(attrs={"class":"form-control"}))
    team_members = forms.CharField(label='Team Members', max_length=1000,widget=forms.Textarea(attrs={'rows':4,"class":"form-control"}))
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=250)
    password = forms.CharField(label='Password', max_length=250)
