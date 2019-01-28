from django.db import models
from decimal import Decimal
import datetime

class Subject(models.Model):
	snum = models.CharField(max_length = 10,unique=True,primary_key=True)
	gender = models.CharField(max_length = 2,default='.')
	dob = models.DateField(default=datetime.date.today)
	retest = models.CharField(max_length=3,default='no') # set to yes for the 20 re-test scans
	def getattribute(self,attr):
		return getattr(self,attr)
	def __str__(self):
		return self.snum 	

# nb: after creating these models I updated the system on 1/22/19 to include where the inclusion categories are more like "pipelines",
# whereas this class was named when I was doing them on a per scan sequence basis
class Sequence(models.Model):
	seq_name = models.CharField(max_length=10,unique=True,primary_key=True)
	subjects = models.ManyToManyField(Subject,through='Inclusion')
	def __str__(self):
		return self.seq_name

# nb: updated on 1/22/19 to include entry for both inclusive and strict list
class Inclusion(models.Model):
	inclusive = models.CharField(max_length=5,null=True,default='.')
	strict = models.CharField(max_length=5,null=True,default='.')
	note = models.CharField(max_length=1000,null=True,default='.')
	subject = models.ForeignKey(Subject,related_name='incval',on_delete=models.DO_NOTHING)
	sequence = models.ForeignKey(Sequence,related_name='incvar',on_delete=models.DO_NOTHING)	
	def __str__(self):
		return self.subject.snum + '_' + self.sequence.seq_name

# class VarGroup(models.Model):
# 	gp_name = models.CharField(max_length=50,unique=True,default='.')
# 	def __str__(self):
# 		return self.gp_name

class HCPMPPVariable(models.Model):
	var_name = models.CharField(max_length=50,unique=True,primary_key=True)
	vargroup = models.CharField(max_length=50,null=True,default='.')
	roi_index = models.IntegerField(default=0)
	subjects = models.ManyToManyField(Subject,through='HCPMPPValue')
	sequence = models.ForeignKey(Sequence,related_name='hcpmppvar',on_delete=models.DO_NOTHING,null=True)
	def __str__(self):
		return self.var_name

class HCPMPPValue(models.Model):
	subject = models.ForeignKey(Subject,related_name='hcpmppval',on_delete=models.DO_NOTHING)
	variable = models.ForeignKey(HCPMPPVariable,on_delete=models.DO_NOTHING)
	value = models.DecimalField(decimal_places=5,max_digits=12,null=True)
	def __str__(self):
		return self.subject.snum + '_' + self.variable.var_name

# class AnatVariable(models.Model):
# 	var_name = models.CharField(max_length=50,unique=True,primary_key=True)
# 	vargroup = models.CharField(max_length=50,null=True,default='.')
# 	subjects = models.ManyToManyField(Subject,through='AnatValue')
# 	sequence = models.ForeignKey(Sequence,related_name='anatvar',on_delete=models.DO_NOTHING,null=True)
# 	def __str__(self):
# 		return self.var_name

# class AnatValue(models.Model):
# 	subject = models.ForeignKey(Subject,related_name='anatval',on_delete=models.DO_NOTHING)
# 	variable = models.ForeignKey(AnatVariable,on_delete=models.DO_NOTHING)
# 	value = models.DecimalField(decimal_places=5,max_digits=12,null=True)
# 	def __str__(self):
# 		return self.subject.snum + '_' + self.variable.var_name

# class FreeSurferVariable(models.Model):
# 	var_name = models.CharField(max_length=50)
# 	vargroup = models.CharField(max_length=50,null=True,default='.')
# 	subjects = models.ManyToManyField(Subject,through='FreeSurferValue')
# 	sequence = models.ForeignKey(Sequence,related_name='freesurfervar',on_delete=models.DO_NOTHING,null=True)
# 	def __str__(self):
# 		return self.var_name

# class FreeSurferValue(models.Model):
# 	subject = models.ForeignKey(Subject,related_name='freesurferval',on_delete=models.DO_NOTHING)
# 	variable = models.ForeignKey(FreeSurferVariable,on_delete=models.DO_NOTHING)
# 	value = models.DecimalField(decimal_places=5,max_digits=16,null=True)
# 	def __str__(self):
# 		return self.subject.snum + '_' + self.variable.var_name

# class FuncROImeanVariable(models.Model):
# 	var_name = models.CharField(max_length=50,unique=True,primary_key=True)
# 	vargroup = models.CharField(max_length=50,null=True,default='.')
# 	subjects = models.ManyToManyField(Subject,through='FuncROImeanValue')
# 	sequence = models.ForeignKey(Sequence,related_name='funcroimeanvar',on_delete=models.DO_NOTHING,null=True)
# 	def __str__(self):
# 		return self.var_name

# class FuncROImeanValue(models.Model):
# 	subject = models.ForeignKey(Subject,related_name='funcroimeanval',on_delete=models.DO_NOTHING)
# 	variable = models.ForeignKey(FuncROImeanVariable,on_delete=models.DO_NOTHING)
# 	value = models.DecimalField(decimal_places=5,max_digits=12,null=True)
# 	def __str__(self):
# 		return self.subject.snum + '_' + self.variable.var_name

# class PathVariable(models.Model):
# 	var_name = models.CharField(max_length=50,unique=True)
# 	vargroup = models.CharField(max_length=50,null=True,default='.')
# 	sequence = models.ForeignKey(Sequence,related_name='path',on_delete=models.DO_NOTHING,null=True)	
# 	path=models.CharField(max_length=500)
# 	def __str__(self):
# 		return self.var_name	


