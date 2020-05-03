from django import forms


class userForm(forms.Form):
    username = forms.CharField(label='User N    ame', max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(placeholder='Password', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(placeholder='E-nail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(placeholder='Phone', max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}))
