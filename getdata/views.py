from django.shortcuts import render, render_to_response
from django.db import models
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import *
from functools import reduce
from django.db.models import Q, Prefetch
from getdata.more_functions import run_query, get_options

from .models import Subject, HCPMPPVariable, Sequence, Inclusion, FuncROImeanVariable, FreeSurferVariable, PathVariable
from .forms import SelectionForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    
# @login_required(login_url="/login/")
# def home(request):
# 	# return render(request, "home.html", {'subjects': Subject.objects.all()})
# 	return render(request, "home.html")

@login_required(login_url="/longdb_dbis/login/")
def select(request):
	if request.method == 'POST':
		form = SelectionForm(request.POST)
		# form_hcpmpp = SelectionForm_hcpmpp(request.POST)

		if form.is_valid(): 
			fields=[]
			if form.cleaned_data['useGender']:
				fields.append('gender')
			if form.cleaned_data['useDOB']:
				fields.append('dob')
			
			#filter(snum__startswith=("0","1")
			subjects = Subject.objects.filter(retest="no").order_by('snum') #[0:10]	########## i guess i get rid of this and just prefetch from each table with the same base query?!?!? wait actually i need subjects to prepopulate blank array; maybe i can make it a queryset or something that i use for each of the following

			fields_hcpmpp,vals_hcpmpp,seqs_hcpmpp=run_query(request.POST.getlist('hcpmpp_selections'),"hcpmpp",subjects)
			fields_funcROImean,vals_funcROImean,seqs_funcROImean=run_query(request.POST.getlist('funcROImean_selections'),"funcroimean",subjects)
			fields_freesurfer,vals_freesurfer,seqs_freesurfer=run_query(request.POST.getlist('freesurfer_selections'),"freesurfer",subjects)
			
			# get the relevant inclusion notes 
			sequences=seqs_hcpmpp+seqs_funcROImean+seqs_freesurfer 
			seq_names=[]
			if(len(sequences)>0):
				sequences=set(sequences) # pare down to just unique values
				seq_names=[s.seq_name for s in sequences]
				subjects_inc=subjects.prefetch_related(  # filter(gender='F').
				    Prefetch(
				            'incval',
				            queryset=Inclusion.objects.filter(reduce(lambda x, y: x | y, [Q(sequence=s) for s in sequences])),
				            to_attr='incvals'
				    )
				)		
				subjects_inc = list(subjects_inc)
				indices=[seq_names.index(subjects_inc[0].incvals[i].sequence_id) for i in range(0,len(seq_names))]
				indices_rev=[indices.index(i) for i in range(0, len(indices))]
				vals_inc=[[s.incvals[i] if i < len(s.incvals) else None for i in indices_rev] for s in subjects_inc] ## if this doesn't work, one subject might be missing required values!! #### this line changes the order of s.anatvals if more than one con_ROI is selected!!!!!				
			else:
				vals_inc=[[] for s in subjects] # need this for zip to work later

			# paths	
			# if(len(equest.POST.getlist('path_selections'))>0):



			subj_data_tuples=list(zip(subjects,vals_inc,vals_hcpmpp,vals_funcROImean, vals_freesurfer))

			if request.POST['action'] == 'Preview':
				#### need to do a bit more research to enable adding the "write csv" button to preview page
				# request.session['context_data'] = {'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_anat':fields_anat,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}
				# print(request.session['context_data'])
				# print('****0******')
				return render(request, 'selected_data.html',{'fields':fields,'seq_names':seq_names,'fields_hcpmpp':fields_hcpmpp,'fields_funcROImean':fields_funcROImean,'fields_freesurfer':fields_freesurfer,'subj_data_tuples':subj_data_tuples})
			else:
				# try:	
				# 	print('********1*********')
				# 	print(fields_day1,subj_data_tuples)
				# 	print(request.session['context_data'])
				# 	subj_data_tuples,fields,fields_anat,fields_day1,fields_bat,fields_snp # check if this is already defined, won't work bc these are defined but empty (excpet subjects)
				# 	context_data = {'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_anat':fields_anat,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}
				# except:
				# 	print('********2*********')
				# 	context_data = request.session['context_data']  # if not, 
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="ExtractedData.csv"'
				t = loader.get_template('write_csv_template.py')
				# response.write(t.render({'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_anat':fields_anat,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}))
				response.write(t.render({'fields':fields,'seq_names':seq_names,'fields_hcpmpp':fields_hcpmpp,'fields_funcROImean':fields_funcROImean,'fields_freesurfer':fields_freesurfer,'subj_data_tuples':subj_data_tuples}))
				return response

		else:
			messages.error(request,"Error", extra_tags='alert')

	else:

		#################### not sure why when i put these in functions, they only return one variable!!
		# options_funcROImean=get_options("funcROImean")
		# options_freesurfer=get_options("freesurfer")		

		options={}
		for fullvar in FreeSurferVariable.objects.all():
			## names are in form task_contrast_ROI.[L/R]
			if fullvar.var_name[-2:]==".L" or fullvar.var_name[-2:]==".R":
				var=fullvar.var_name[:-2]
			else:
				var=fullvar.var_name
			vargroup=fullvar.vargroup
			if vargroup not in options:
				options[vargroup]=[]
			if var not in options[vargroup]:
				options[vargroup].append(var)
		options_freesurfer=options

		options={}
		for fullvar in FuncROImeanVariable.objects.all():
			## names are in form task_contrast_ROI.[L/R]
			if fullvar.var_name[-2:]==".L" or fullvar.var_name[-2:]==".R":
				var=fullvar.var_name[:-2]
			else:
				var=fullvar.var_name
			vargroup=fullvar.vargroup
			if vargroup not in options:
				options[vargroup]=[]
			if var not in options[vargroup]:
				options[vargroup].append(var)
		options_funcROImean=options

		options={}
		for var in PathVariable.objects.all():
			vargroup=var.vargroup
			if vargroup not in options:
				options[vargroup]=[]
			if var not in options[vargroup]:
				options[vargroup].append(var)
		options_path=options

		vargroups=HCPMPPVariable.objects.all().values("vargroup").annotate(n=models.Count("pk"))#[0]['vargroup'] # get unique values of vargroup
		options_hcpmpp=[]
		for vargroup in vargroups:
			options_hcpmpp.append(vargroup['vargroup'])

		form = SelectionForm()

	return render(request, 'select.html',{'form':form,'options_hcpmpp':options_hcpmpp,'options_funcROImean':options_funcROImean,'options_freesurfer':options_freesurfer,'options_path':options_path})


