from django.contrib import admin
from .models import Subject, HCPMPPVariable, HCPMPPValue, Sequence, Inclusion #, FuncROImeanVariable, FuncROImeanValue, PathVariable

admin.site.register(Subject)
# admin.site.register(FuncROImeanVariable)
# admin.site.register(FuncROImeanValue)
admin.site.register(HCPMPPValue)
admin.site.register(HCPMPPVariable)
admin.site.register(Sequence)
admin.site.register(Inclusion)
# admin.site.register(PathVariable)
