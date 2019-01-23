from .models import HCPMPPVariable, FuncROImeanVariable, FreeSurferVariable, HCPMPPValue, FuncROImeanValue, FreeSurferValue
from django.db.models import Q, Prefetch
from functools import reduce


def get_subvars(var,var_type):
	if var_type == "hcpmpp":
		allvars=HCPMPPVariable.objects.all().order_by('roi_index')
		use_group="yes"
	elif var_type == "funcroimean":
		allvars=FuncROImeanVariable.objects.all()
		use_group="no"
	elif var_type == "freesurfer":
		allvars=FreeSurferVariable.objects.all()
		use_group="no"
	else:
		print("Invalid var_type: "+var_type)
		return
	if use_group == "yes":
		varlist=list(allvars.filter(vargroup=var).values_list('var_name',flat=True)) # might want to put order_by(index) here??
	else:	
		varlist=[]
		for v in allvars:
			if v.var_name.startswith(var):
				varlist.append(v.var_name)
	return varlist	

def run_query(requested_vars,var_type,subjects):
	if var_type == "hcpmpp":
		allvars=HCPMPPVariable.objects
		allvals=HCPMPPValue.objects
	elif var_type == "funcroimean":
		allvars=FuncROImeanVariable.objects
		allvals=FuncROImeanValue.objects
	elif var_type == "freesurfer":
		allvars=FreeSurferVariable.objects
		allvals=FreeSurferValue.objects
	else:
		print("Invalid var_type: "+var_type)
		return	
	related_name=var_type+'val'
	vars_out=[]
	fields_out=[]
	sequences=[]
	for requested_var in requested_vars:
		#print("reqvar"+requested_var)
		for subvar in get_subvars(requested_var,var_type):
			#print("subvar"+subvar)
			vars_out.append(allvars.get(var_name=subvar))  
			fields_out.append(subvar)
			sequences.append(allvars.get(var_name=subvar).sequence) #.seq_name
	if(len(vars_out)>0):
		subjects_out=subjects.prefetch_related(  # filter(gender='F').
		    Prefetch(
		            related_name,
		            queryset=allvals.filter(reduce(lambda x, y: x | y, [Q(variable=v) for v in vars_out])),
		            to_attr='fetched_vals'
		    )
		)		
		subjects_out = list(subjects_out)
		# print("HI")
		# print(subjects_out[0].fetched_vals )
		# for i in range(0,len(fields_out)):
		# 	print(subjects_out[0].fetched_vals[i].variable_id)
		indices=[fields_out.index(subjects_out[0].fetched_vals[i].variable_id) for i in range(0,len(fields_out))]  #### if this isn't working, it might be because the first subject does not have values for the given variable, and you need to create null ones!
		indices_rev=[indices.index(i) for i in range(0, len(indices))]
		vals_out=[[s.fetched_vals[i] if i < len(s.fetched_vals) else None for i in indices_rev] for s in subjects_out] ###### this line changes the order of s.fetched_vals if more than one con_ROI is selected!!!!!				
	else:
		vals_out=[[] for s in subjects] # need this for zip to work later
	return fields_out,vals_out,sequences

def get_options(var_type):
	if var_type == "anat":
		allvars=AnatVariable.objects.all()
	elif var_type == "funcROImean":
		allvars=FuncROImeanVariable.objects.all()
	elif var_type == "freesurfer":
		allvars=FreeSurferVariable.objects.all()
	else:
		print("Invalid var_type: "+var_type)
		return	
	options={}
	for fullvar in allvars:
		## names are in form task_contrast_ROI.[L/R]
		if fullvar.var_name[-2:]==".L" or fullvar.var_name[-2:]==".R":
			var=fullvar.var_name[:-2]
		else:
			var=fullvar.var_name
		print(var)
		vargroup=fullvar.vargroup
		if vargroup not in options:
			options[vargroup]=[]
		if var not in options[vargroup]:
			options[vargroup].append(var)
		return options



