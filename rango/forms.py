from django import forms
from rango.models import UserProfile, Page, Category
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    #an inlien class to priide additional information on the forms
    class Meta:
        #provvide an association btw ModelForm and model
        model = Category

class PageForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page

        '''what field do we want to nclude in our form?
        this way we don't need every filed in the model present
        some fields may allow NULL values, so we may not want to include them...
        here we're hidng hte foreign key'''
        fields = ('title', 'url', 'views')

    def clean(self):
            cleaned_data = self.cleaned_data
            url = cleaned_data.get('url')

            # If url is not empty and doesn't start with 'http://', prepend 'http://'.
            if url and not url.startswith('http://'):
                url = 'http://' + url
                cleaned_data['url'] = url

            return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

