basedir='/home6/haririla/public_html/longdb_dbis'

## run these from within a django shell:
## python3 manage.py shell	 (and then paste in), or:
## python3 manage.py shell < importing_data_scratch.py	


# # imaging data - FreeSurfer
################ need to add sequence to each variable!!!!!!!!!
# import datetime, csv
# from decimal import Decimal
# from getdata.models import Subject, AnatVariable, AnatValue
# with open('/Users/Annchen/DjangoProjects/longdb_dbis/DataToIncorporate/FreeSurfer_aparc.DKTatlas_GrayVol.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	for row in reader:
# 		print(row[0])
# 		s,c=Subject.objects.get_or_create(snum=row[0].replace("DMHDS",""))
# 		for i in range(1,len(row1)):
# 			r,c=AnatVariable.objects.get_or_create(var_name=row1[i])
# 			if(row[i]):
# 				g=AnatValue.objects.create(subject=s,variable=r,value=row[i])			
# 			else:
# 				g=AnatValue.objects.create(subject=s,variable=r,value=None)			

# # imaging data - func ROI
# ## ##Func Variable names (column headings) MUST be of the format ROI_Contrast!!!!!!!!
# ############### need to add sequence to each variable!!!!!!!!!
# import datetime, csv
# from decimal import Decimal
# from getdata.models import Subject, FuncROImeanVariable, FuncROImeanValue, Sequence
# task="Faces" ################
# seq=Sequence.objects.get(seq_name="facename")
# with open('/Users/Annchen/DjangoProjects/longdb_dbis/DataToIncorporate/fMRI_ROImeans_faces_glm_AFNI_splitRuns.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	for row in reader:
# 		print(row[0])
# 		s,c=Subject.objects.get_or_create(snum=row[0].replace("DMHDS",""))
# 		for i in range(1,len(row1)):
# 			roi,con=row1[i].split('_')
# 			r,c=FuncROImeanVariable.objects.get_or_create(var_name=task+"_"+con+"_"+roi,sequence=seq,vargroup=task)
# 			if(row[i]):
# 				if(row[i]=="NA"):
# 					g=FuncROImeanValue.objects.create(subject=s,variable=r,value=None)			
# 				else:
# 					g=FuncROImeanValue.objects.create(subject=s,variable=r,value=row[i])			
# 			else:
# 				g=FuncROImeanValue.objects.create(subject=s,variable=r,value=None)			

# ## FreeSurfer
# import datetime, csv
# import glob
# from decimal import Decimal
# from getdata.models import Subject, Sequence, FreeSurferValue, FreeSurferVariable
# seq=Sequence.objects.get(seq_name="t1")
# print(glob.glob("/home/adam/*.txt"))
# files=glob.glob('/Users/Annchen/DjangoProjects/longdb_dbis/DataToIncorporate/FreeSurfer/Free*.csv')
# for file in files[30:]:
# 	skipfile=0
# 	print(file)
# 	task=file.split('/')[-1].replace('.csv','')
# 	with open(file,newline='') as f:
# 		reader=csv.reader(f)
# 		row1=next(reader)
# 		for row in reader:
# 			if skipfile==1:
# 				break
# 			# print(row[0])
# 			s,c=Subject.objects.get_or_create(snum=row[0].replace("DMHDS",""))
# 			for i in range(1,len(row1)):
# 				if 'aseg' in file:
# 					if 'Right-' in row1[i]:
# 						roi=row1[i].replace('Right-','')+'.R'
# 					elif 'Left-' in row1[i]:
# 						roi=row1[i].replace('Left-','')+'.L'
# 				elif 'wmparc' in file:
# 					if 'wm-lh' in row1[i]:
# 						roi=row1[i].replace('wm-lh','wm')+'.L'
# 					elif 'wm-rh' in row1[i]:
# 						roi=row1[i].replace('wm-rh','wm')+'.R'	
# 				else:
# 					roi=row1[i].replace('_left','.L').replace('_right','.R')
# 				try:
# 					r,c=FreeSurferVariable.objects.get_or_create(var_name=roi,sequence=seq,vargroup=task)
# 					if(row[i]):
# 						if(row[i]=="NA"):
# 							g=FreeSurferValue.objects.create(subject=s,variable=r,value=None)			
# 						else:
# 							g=FreeSurferValue.objects.create(subject=s,variable=r,value=row[i])			
# 					else:
# 						g=FreeSurferValue.objects.create(subject=s,variable=r,value=None)		
# 				except:
# 					print("Error with "+s.snum+" "+roi)
# 					skipfile=1
# 					break


### Inclusion data
## second round, with HCP
#import csv
#from getdata.models import Subject, Sequence, Inclusion
#r,c=Sequence.objects.get_or_create(seq_name="HCPMPP")
#with open(basedir+'/DataToIncorporate/LOG_master_inclusion_list.csv',newline='') as f:
#	reader=csv.reader(f)
#	row1=next(reader)
#	for row in reader:
#		# print(row)
#		s,c=Subject.objects.get_or_create(snum=row[0].replace("DMHDS",""))
#		### assuming all fields are non-empty - check before importing!!!!!
#		g=Inclusion.objects.create(subject=s,sequence=r,inclusive=row[4],strict=row[5],note=row[6])			
## first round
# import datetime, csv
# # from getdata.models import Subject, Sequence, Inclusion
# with open('/Users/Annchen/DjangoProjects/longdb_dbis/DataToIncorporate/LOG_master_inclusion_list.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	for row in reader:
# 		# print(row)
# 		# s,c=Subject.objects.get_or_create(snum=row[0].replace("DMHDS",""))
# 		for i in range(1,len(row1)):
# 			# r,c=Sequence.objects.get_or_create(seq_name=row1[i].replace("_ok",""))
# 			if(row[i]):
# 				#### finish this logic later
# 				# if ":" in row[i]:
# 				# 	code=row[i].split(":",1)[0]
# 				# 	note=row[i].split(":",1)[1]
# 				# 	if "|" in note:
# 				# 		n1=note.split("|",3)[0][1]
# 				# 		n2=note.split("|",3)[1][1]
# 				# 		n3=note.split("|",3)[2][1]
# 				# 		n4=note.split("|",3)[3][1]
# 				# 		print("code: "+code+" n1: "+n1+" n2: "+n2+" n3: "+n3+" n4: "+n4)
# 				g=Inclusion.objects.create(subject=s,sequence=r,note=row[i])			
# 			else:
# 				g=Inclusion.objects.create(subject=s,sequence=r,note=None)		

### demo data
import csv
from getdata.models import Subject
with open(basedir+'/DataToIncorporate/ImagingBaseFile_forDB.csv',newline='') as f:
	reader=csv.reader(f)
	row1=next(reader)
	for row in reader:
		try:
			s=Subject.objects.get(snum=row[0].replace("sub-",""))
			s.gender=row[1]
			s.save()
		except:
			print("no subject: "+row[0])

### imaging data - HCPMPP
#import csv
#from getdata.models import Subject, HCPMPPVariable, HCPMPPValue, Sequence
#seq,c=Sequence.objects.get_or_create(seq_name="HCPMPP")
#with open(basedir+'/DataToIncorporate/corrCT_HCPMPP.csv',newline='') as f:
#	reader=csv.reader(f)
#	row1=next(reader)
#	for row in reader:
#		print(row[0])
#		s,c=Subject.objects.get_or_create(snum=row[1].replace("sub-",""))
#		for i in range(2,len(row1)):
#			r,c=HCPMPPVariable.objects.get_or_create(var_name="HCPMPP_Glasser_"+row1[i],roi_index=i-2,sequence=seq,vargroup="HCPMPP_Glasser_CorticalThickness")
#			if(row[i]):
#				g=HCPMPPValue.objects.create(subject=s,variable=r,value=row[i])			
#			else:
#				g=HCPMPPValue.objects.create(subject=s,variable=r,value=None)	

# # fill in "sequence" values
# from getdata.models import Sequence, AnatVariable
# imgvars=AnatVariable.objects.all()
# s=Sequence.objects.get(seq_name="t1") 
# for v in imgvars:
# 	v.sequence=s
# 	v.save()

# # fill in NULL img values
# ### MUST run this if the csv file used for importing imaging data only includes subjects with good data
# from getdata.models import Subject, AnatVariable, AnatValue, FuncROImeanValue, FuncROImeanVariable
# subjects=Subject.objects.all()
# imgvars=FuncROImeanVariable.objects.all()
# for s in subjects:
# 	for v in imgvars:
# 		# check if exists
# 		found=FuncROImeanValue.objects.filter(subject=s,variable=v)
# 		if found.count() == 0:
# 			FuncROImeanValue.objects.create(subject=s,variable=v,value=None)

