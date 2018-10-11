from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from .models import AnatVariable #, FuncVariable

class SelectionForm(forms.Form):
	useGender = forms.BooleanField(required=False,label='Gender') #,initial='True'
	useDOB = forms.BooleanField(required=False,label='Birth Date')


class SelectionForm_Anat(forms.Form):
	fullnames=[v.var_name.split('_',1)[0] for v in AnatVariable.objects.all()] # use split to pull only the measure name
	names=sorted(set(fullnames)) # get unique entries (i.e. one for each measure)
	OPTIONS=zip(names,names)
	anat_selections = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':10,'cols':30}),choices=OPTIONS,required=False,label='')	

# class SelectionForm_Func(forms.Form):
# 	fullnames=[v.var_name.split('_',1)[0] for v in BatteryVariable.objects.all()] # use split to pull only the measure name
# 	names=sorted(set(fullnames)) # get unique entries (i.e. one for each measure)
# 	OPTIONS=zip(names,names)
# 	func_selections = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':10,'cols':15}),choices=OPTIONS,required=False,label='')	



# # add this to allow bootstrap css
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label="Username", max_length=30, 
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
#     password = forms.CharField(label="Password", max_length=30, 
#                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


# class SelectionForm_Imaging(forms.Form):
# 	useAmygdala = forms.BooleanField(required=False,label='Amygdala')
# 	useVS = forms.BooleanField(required=False,label='VS')